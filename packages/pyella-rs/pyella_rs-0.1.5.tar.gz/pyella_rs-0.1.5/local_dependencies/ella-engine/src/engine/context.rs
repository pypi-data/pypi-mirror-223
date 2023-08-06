use std::{fmt::Debug, ops::DerefMut, sync::Arc};

use tokio::sync::Mutex;

use crate::{
    catalog::EllaCatalog,
    cluster::EllaCluster,
    config::EllaConfig,
    engine::EllaState,
    lazy::Lazy,
    registry::{Id, SchemaRef, TableRef},
    schema::EllaSchema,
    table::{
        info::{TableInfo, TopicInfo, ViewInfo},
        EllaTable, EllaTopic, EllaView,
    },
};

use super::Engine;

#[derive(Clone)]
pub struct EllaContext {
    state: EllaState,
    engine: Arc<Mutex<Option<Engine>>>,
}

impl Debug for EllaContext {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("EllaContext")
            .field("state", &self.state)
            .field("engine", &self.engine)
            .finish_non_exhaustive()
    }
}

impl EllaContext {
    pub fn new(state: EllaState) -> crate::Result<Self> {
        let engine = Arc::new(Mutex::new(Some(Engine::start(Arc::new(state.clone()))?)));
        Ok(Self { state, engine })
    }

    pub fn use_catalog<'a>(mut self, catalog: impl Into<Id<'a>>) -> crate::Result<Self> {
        let catalog: Id<'static> = catalog.into().into_owned();

        self.cluster()
            .catalog(catalog.as_ref())
            .ok_or_else(|| crate::EngineError::CatalogNotFound(catalog.to_string()))?;

        let config = self
            .state
            .config()
            .clone()
            .into_builder()
            .default_catalog(catalog)
            .build();
        self.state.with_config(config);
        Ok(self)
    }

    pub fn use_schema<'a>(mut self, schema: impl Into<Id<'a>>) -> crate::Result<Self> {
        let schema: Id<'static> = schema.into().into_owned();

        self.cluster()
            .catalog(self.default_catalog())
            .ok_or_else(|| crate::EngineError::CatalogNotFound(self.default_catalog().to_string()))?
            .schema(schema.as_ref())
            .ok_or_else(|| crate::EngineError::SchemaNotFound(schema.to_string()))?;

        let config = self
            .state
            .config()
            .clone()
            .into_builder()
            .default_schema(schema)
            .build();
        self.state.with_config(config);
        Ok(self)
    }

    pub async fn query(&self, sql: impl AsRef<str>) -> crate::Result<Lazy> {
        self.state.query(sql).await
    }

    pub async fn execute(&self, sql: &str) -> crate::Result<()> {
        self.query(sql).await?.execute().await?;
        Ok(())
    }

    pub async fn create_topic<'a>(
        &self,
        table: impl Into<TableRef<'a>>,
        info: impl Into<TopicInfo>,
        if_not_exists: bool,
        or_replace: bool,
    ) -> crate::Result<Arc<EllaTopic>> {
        self.state
            .create_topic(
                self.state.resolve(table.into()),
                info.into(),
                if_not_exists,
                or_replace,
            )
            .await
    }

    pub async fn create_view<'a>(
        &self,
        table: impl Into<TableRef<'a>>,
        info: impl Into<ViewInfo>,
        if_not_exists: bool,
        or_replace: bool,
    ) -> crate::Result<Arc<EllaView>> {
        self.state
            .create_view(
                self.state.resolve(table.into()),
                info.into(),
                if_not_exists,
                or_replace,
            )
            .await
    }

    pub async fn create_table<'a>(
        &self,
        table: impl Into<TableRef<'a>>,
        info: impl Into<TableInfo>,
        if_not_exists: bool,
        or_replace: bool,
    ) -> crate::Result<Arc<EllaTable>> {
        self.state
            .create_table(
                self.state.resolve(table.into()),
                info.into(),
                if_not_exists,
                or_replace,
            )
            .await
    }

    pub async fn create_schema<'a>(
        &self,
        schema: impl Into<SchemaRef<'a>>,
        if_not_exists: bool,
    ) -> crate::Result<Arc<EllaSchema>> {
        self.state.create_schema(schema, if_not_exists).await
    }

    pub async fn create_catalog<'a>(
        &self,
        catalog: impl Into<Id<'a>>,
        if_not_exists: bool,
    ) -> crate::Result<Arc<EllaCatalog>> {
        self.state.create_catalog(catalog, if_not_exists).await
    }

    pub fn table<'a>(&self, table: impl Into<TableRef<'a>>) -> Option<Arc<EllaTable>> {
        self.state.table(self.state.resolve(table.into()))
    }

    pub async fn shutdown(self) -> crate::Result<()> {
        if let Some(engine) = std::mem::take(self.engine.lock_owned().await.deref_mut()) {
            engine.shutdown().await?;
        }
        Ok(())
    }

    pub fn config(&self) -> &EllaConfig {
        self.state.config()
    }

    pub fn cluster(&self) -> &Arc<EllaCluster> {
        self.state.cluster()
    }

    pub fn default_catalog(&self) -> &Id<'static> {
        self.state.default_catalog()
    }

    pub fn default_schema(&self) -> &Id<'static> {
        self.state.default_schema()
    }

    pub fn state(&self) -> &EllaState {
        &self.state
    }
}
