use std::{fmt::Debug, sync::Arc};

use datafusion::{
    error::DataFusionError,
    execution::{context::SessionState, runtime_env::RuntimeEnv},
    prelude::SessionConfig,
};
use object_store::ObjectStore;

use crate::{
    catalog::EllaCatalog,
    cluster::EllaCluster,
    codec::EllaExtensionCodec,
    config::EllaConfig,
    lazy::{Lazy, LocalBackend},
    registry::{Id, SchemaRef, TableId, TableRef, TransactionLog},
    schema::EllaSchema,
    table::{
        info::{TableInfo, TopicInfo, ViewInfo},
        EllaTable, EllaTopic, EllaView,
    },
    Path, Plan,
};

#[derive(Clone)]
pub struct EllaState {
    root: Path,
    log: Arc<TransactionLog>,
    store: Arc<dyn ObjectStore + 'static>,
    cluster: Arc<EllaCluster>,
    session: SessionState,
    config: EllaConfig,
}

impl Debug for EllaState {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("EllaState")
            .field("log", &self.log)
            .field("cluster", &self.cluster)
            .field("config", &self.config)
            .finish_non_exhaustive()
    }
}

impl EllaState {
    const LOG: &'static str = ".ella";

    pub(crate) async fn open(root: &str) -> crate::Result<Self> {
        let root: crate::Path = root.parse()?;
        let env = Arc::new(RuntimeEnv::default());
        let store = env.object_store(&root)?;
        let log = Arc::new(TransactionLog::new(root.join(Self::LOG), store.clone()));

        let config = log.load_config().await?;
        let cluster = Arc::new(EllaCluster::new(log.clone(), root.clone()));
        let session = Self::make_session(cluster.clone(), env, &config);

        let this = Self {
            root,
            log,
            store,
            cluster,
            session,
            config,
        };
        this.restore().await?;
        Ok(this)
    }

    pub(crate) async fn create(
        root: &str,
        config: EllaConfig,
        if_not_exists: bool,
    ) -> crate::Result<Self> {
        let root: crate::Path = root.parse()?;
        let env = Arc::new(RuntimeEnv::default());
        let store = env.object_store(&root)?;
        let log = Arc::new(TransactionLog::new(root.join(Self::LOG), store.clone()));

        let config = match (if_not_exists, log.load_config().await) {
            (true, Ok(config)) => config,
            (false, Ok(_)) => {
                return Err(crate::EngineError::DatastoreExists(root.to_string()).into())
            }
            (_, Err(_)) => {
                log.create(config.clone()).await?;
                config
            }
        };

        let cluster = Arc::new(EllaCluster::new(log.clone(), root.clone()));
        let session = Self::make_session(cluster.clone(), env, &config);

        let this = Self {
            root,
            log,
            store,
            cluster,
            session,
            config,
        };
        this.restore().await?;
        Ok(this)
    }

    pub fn with_config(&mut self, config: EllaConfig) {
        self.session = Self::make_session(
            self.cluster.clone(),
            self.session.runtime_env().clone(),
            &config,
        );
        self.config = config;
    }

    fn make_session(
        cluster: Arc<EllaCluster>,
        runtime: Arc<RuntimeEnv>,
        config: &EllaConfig,
    ) -> SessionState {
        let config = SessionConfig::new()
            .with_information_schema(true)
            .with_create_default_catalog_and_schema(false)
            .with_default_catalog_and_schema(
                config.default_catalog().to_string(),
                config.default_schema().to_string(),
            )
            // TODO: support repartitioning
            .with_round_robin_repartition(false)
            // TODO: support batches
            .with_coalesce_batches(false);

        SessionState::with_config_rt_and_catalog_list(config, runtime, cluster)
    }

    async fn restore(&self) -> crate::Result<()> {
        let snapshot = self.log.load_snapshot().await?;
        self.cluster.load(&snapshot, self)?;

        // Create default catalog and schema if they don't already exist
        let catalog = self
            .cluster()
            .create_catalog(self.config().default_catalog().clone(), true)
            .await?;
        catalog
            .create_schema(self.config().default_schema().clone(), true)
            .await?;

        Ok(())
    }

    pub async fn query(&self, sql: impl AsRef<str>) -> crate::Result<Lazy> {
        let plan = self.session.create_logical_plan(sql.as_ref()).await?;
        Ok(Lazy::new(Plan::from_plan(plan), Arc::new(self.backend())))
    }

    pub async fn create_topic(
        &self,
        id: TableId<'static>,
        info: TopicInfo,
        if_not_exists: bool,
        or_replace: bool,
    ) -> crate::Result<Arc<EllaTopic>> {
        let schema = self
            .cluster()
            .catalog(&id.catalog)
            .ok_or_else(|| crate::EngineError::CatalogNotFound(id.catalog.to_string()))?
            .schema(&id.schema)
            .ok_or_else(|| crate::EngineError::SchemaNotFound(id.schema.to_string()))?;

        let table = self.table((&id).into());
        match (if_not_exists, or_replace, table) {
            // table exists, return as-is
            (true, false, Some(table)) => match table.as_topic() {
                Some(topic) => Ok(topic),
                None => Err(DataFusionError::Execution(format!(
                    "table {} exists but is a view not a topic",
                    id
                ))
                .into()),
            },
            // table exists, replace table
            (false, true, Some(_)) => {
                let topic = Arc::new(EllaTopic::new(id.clone(), info, self)?);
                schema.drop_table(&id.table, true).await?;

                schema
                    .register(id.table, Arc::new(topic.clone().into()))
                    .await?;
                Ok(topic)
            }
            (true, true, Some(_)) => Err(DataFusionError::Execution(
                "IF NOT EXISTS and REPLACE cannot both be specified".to_string(),
            )
            .into()),
            // create table
            (_, _, None) => {
                let topic = Arc::new(EllaTopic::new(id.clone(), info, self)?);
                schema
                    .register(id.table, Arc::new(topic.clone().into()))
                    .await?;
                Ok(topic)
            }
            // table exists
            (false, false, Some(_)) => Err(crate::EngineError::TableExists(id.to_string()).into()),
        }
    }

    pub async fn create_view(
        &self,
        id: TableId<'static>,
        info: ViewInfo,
        if_not_exists: bool,
        or_replace: bool,
    ) -> crate::Result<Arc<EllaView>> {
        let schema = self
            .cluster()
            .catalog(&id.catalog)
            .ok_or_else(|| crate::EngineError::CatalogNotFound(id.catalog.to_string()))?
            .schema(&id.schema)
            .ok_or_else(|| crate::EngineError::SchemaNotFound(id.schema.to_string()))?;

        let table = self.table((&id).into());
        match (if_not_exists, or_replace, table) {
            // table exists, return as-is
            (true, false, Some(table)) => match table.as_view() {
                Some(view) => Ok(view),
                None => Err(DataFusionError::Execution(format!(
                    "table {} exists but is a topic not a view",
                    id
                ))
                .into()),
            },
            // table exists, replace table
            (false, true, Some(_)) => {
                let view = Arc::new(EllaView::new(id.clone(), info, self, true)?);
                schema.drop_table(&id.table, true).await?;

                schema
                    .register(id.table, Arc::new(view.clone().into()))
                    .await?;
                Ok(view)
            }
            (true, true, Some(_)) => Err(DataFusionError::Execution(
                "IF NOT EXISTS and REPLACE cannot both be specified".to_string(),
            )
            .into()),
            // create table
            (_, _, None) => {
                let view = Arc::new(EllaView::new(id.clone(), info, self, true)?);
                schema
                    .register(id.table, Arc::new(view.clone().into()))
                    .await?;
                Ok(view)
            }
            // table exists
            (false, false, Some(_)) => Err(crate::EngineError::TableExists(id.to_string()).into()),
        }
    }

    pub async fn create_table(
        &self,
        id: TableId<'static>,
        info: TableInfo,
        if_not_exists: bool,
        or_replace: bool,
    ) -> crate::Result<Arc<EllaTable>> {
        match info {
            TableInfo::Topic(info) => Ok(Arc::new(
                self.create_topic(id, info, if_not_exists, or_replace)
                    .await?
                    .into(),
            )),
            TableInfo::View(info) => Ok(Arc::new(
                self.create_view(id, info, if_not_exists, or_replace)
                    .await?
                    .into(),
            )),
        }
    }

    pub fn table(&self, table: TableId<'_>) -> Option<Arc<EllaTable>> {
        self.cluster
            .catalog(table.catalog)?
            .schema(table.schema)?
            .table(table.table)
    }

    pub async fn create_catalog<'a>(
        &self,
        catalog: impl Into<Id<'a>>,
        if_not_exists: bool,
    ) -> crate::Result<Arc<EllaCatalog>> {
        self.cluster().create_catalog(catalog, if_not_exists).await
    }

    pub async fn create_schema<'a>(
        &self,
        schema: impl Into<SchemaRef<'a>>,
        if_not_exists: bool,
    ) -> crate::Result<Arc<EllaSchema>> {
        let schema: SchemaRef<'a> = schema.into();
        let schema = schema.resolve(self.default_catalog());
        let catalog = self
            .cluster
            .catalog(&schema.catalog)
            .ok_or_else(|| crate::EngineError::CatalogNotFound(schema.catalog.to_string()))?;
        catalog.create_schema(schema.schema, if_not_exists).await
    }

    pub fn resolve(&self, table: TableRef<'_>) -> TableId<'static> {
        table.resolve(self.default_catalog(), self.default_schema())
    }

    pub fn log(&self) -> &Arc<TransactionLog> {
        &self.log
    }

    pub fn root(&self) -> &Path {
        &self.root
    }

    pub fn session(&self) -> &SessionState {
        &self.session
    }

    pub fn cluster(&self) -> &Arc<EllaCluster> {
        &self.cluster
    }

    pub fn store(&self) -> &Arc<dyn ObjectStore + 'static> {
        &self.store
    }

    pub fn config(&self) -> &EllaConfig {
        &self.config
    }

    pub fn default_catalog(&self) -> &Id<'static> {
        self.config.default_catalog()
    }

    pub fn default_schema(&self) -> &Id<'static> {
        self.config.default_schema()
    }

    pub fn codec(&self) -> EllaExtensionCodec {
        EllaExtensionCodec::new(self.cluster.clone())
    }

    #[doc(hidden)]
    pub fn backend(&self) -> LocalBackend {
        LocalBackend::new(self.clone())
    }
}
