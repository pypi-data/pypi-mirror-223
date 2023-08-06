mod publisher;

pub use publisher::Publisher;

use std::{future::IntoFuture, sync::Arc};

use ella_engine::{
    registry::{TableId, TableRef},
    table::{info::TableInfo, EllaTable},
};
use ella_server::table::RemoteTable;
use futures::{future::BoxFuture, FutureExt};

use crate::Ella;

#[derive(Debug)]
pub struct Table {
    inner: TableInner,
}

#[derive(Debug)]
enum TableInner {
    Local(Arc<EllaTable>),
    Remote(RemoteTable),
}

impl Table {
    pub(crate) fn local(table: Arc<EllaTable>) -> Self {
        Self {
            inner: TableInner::Local(table),
        }
    }

    pub(crate) fn remote(table: RemoteTable) -> Self {
        Self {
            inner: TableInner::Remote(table),
        }
    }

    pub fn publish(&self) -> crate::Result<Publisher> {
        use TableInner::*;
        Ok(match &self.inner {
            Local(table) => match table.as_topic() {
                Some(topic) => Publisher::new(topic.publish(), topic.info().arrow_schema()),
                None => todo!(),
            },
            Remote(table) => Publisher::new(table.publish(), table.arrow_schema()?),
        })
    }

    pub fn id(&self) -> &TableId<'static> {
        use TableInner::*;
        match &self.inner {
            Local(table) => table.id(),
            Remote(table) => table.id(),
        }
    }

    pub fn info(&self) -> TableInfo {
        use TableInner::*;
        match &self.inner {
            Local(table) => table.info(),
            Remote(table) => table.info(),
        }
    }
}

#[must_use]
#[derive(Debug)]
pub struct GetTable<'a> {
    inner: &'a Ella,
    table: TableRef<'a>,
}

impl<'a> GetTable<'a> {
    pub(crate) fn new(inner: &'a Ella, table: TableRef<'a>) -> Self {
        Self { inner, table }
    }

    pub fn or_create(self, info: impl Into<TableInfo>) -> GetOrCreateTable<'a> {
        GetOrCreateTable {
            inner: self.inner,
            table: self.table,
            info: info.into(),
        }
    }

    pub fn replace(self, info: impl Into<TableInfo>) -> CreateOrReplaceTable<'a> {
        CreateOrReplaceTable(CreateTable {
            inner: self.inner,
            table: self.table,
            info: info.into(),
        })
    }

    pub fn drop(self) -> DropTable<'a> {
        DropTable {
            inner: self.inner,
            table: self.table,
            if_exists: false,
        }
    }
}

impl<'a> IntoFuture for GetTable<'a> {
    type Output = crate::Result<Option<crate::Table>>;
    type IntoFuture = BoxFuture<'a, crate::Result<Option<crate::Table>>>;

    fn into_future(self) -> Self::IntoFuture {
        self.inner.get_table(self.table).boxed()
    }
}

#[must_use]
#[derive(Debug)]
pub struct GetOrCreateTable<'a> {
    inner: &'a Ella,
    table: TableRef<'a>,
    info: TableInfo,
}

impl<'a> IntoFuture for GetOrCreateTable<'a> {
    type Output = crate::Result<crate::Table>;
    type IntoFuture = BoxFuture<'a, Self::Output>;

    fn into_future(self) -> Self::IntoFuture {
        async move {
            Ok(match self.inner.get_table(self.table.clone()).await? {
                Some(table) => table,
                None => {
                    self.inner
                        .create_table(self.table, self.info, true, false)
                        .await?
                }
            })
        }
        .boxed()
    }
}

#[must_use]
#[derive(Debug)]
pub struct CreateTable<'a> {
    inner: &'a Ella,
    table: TableRef<'a>,
    info: TableInfo,
}

impl<'a> CreateTable<'a> {
    pub fn if_not_exists(self) -> GetOrCreateTable<'a> {
        GetOrCreateTable {
            inner: self.inner,
            table: self.table,
            info: self.info,
        }
    }

    pub fn or_replace(self) -> CreateOrReplaceTable<'a> {
        CreateOrReplaceTable(self)
    }
}

impl<'a> IntoFuture for CreateTable<'a> {
    type Output = crate::Result<crate::Table>;
    type IntoFuture = BoxFuture<'a, Self::Output>;

    fn into_future(self) -> Self::IntoFuture {
        async move {
            self.inner
                .create_table(self.table, self.info, false, false)
                .await
        }
        .boxed()
    }
}

#[must_use]
#[derive(Debug)]
pub struct CreateOrReplaceTable<'a>(CreateTable<'a>);

impl<'a> IntoFuture for CreateOrReplaceTable<'a> {
    type Output = crate::Result<crate::Table>;
    type IntoFuture = BoxFuture<'a, Self::Output>;

    fn into_future(self) -> Self::IntoFuture {
        async move {
            self.0
                .inner
                .create_table(self.0.table, self.0.info, false, true)
                .await
        }
        .boxed()
    }
}

#[must_use]
#[derive(Debug)]
pub struct DropTable<'a> {
    inner: &'a Ella,
    table: TableRef<'a>,
    if_exists: bool,
}

impl<'a> DropTable<'a> {
    pub fn if_exists(mut self) -> Self {
        self.if_exists = true;
        self
    }
}

impl<'a> IntoFuture for DropTable<'a> {
    type Output = crate::Result<&'a Ella>;
    type IntoFuture = BoxFuture<'a, Self::Output>;

    fn into_future(self) -> Self::IntoFuture {
        async move {
            let if_exists = if self.if_exists { "IF EXISTS " } else { "" };
            self.inner
                .execute(format!("DROP TABLE {if_exists}{}", self.table))
                .await?;

            Ok(self.inner)
        }
        .boxed()
    }
}
