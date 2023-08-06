mod context;
mod state;

pub use context::EllaContext;
pub use state::EllaState;

use std::{fmt::Debug, sync::Arc};

use crate::util::Maintainer;

#[derive(Debug)]
pub struct Engine {
    state: Arc<EllaState>,
    maintainer: Maintainer,
    #[cfg(feature = "metrics")]
    metrics: Option<crate::metrics::MetricsServer>,
}

impl Engine {
    pub(crate) fn start(state: Arc<EllaState>) -> crate::Result<Self> {
        let config = state.config().engine_config();
        let maintainer = Maintainer::new(state.clone(), config.maintenance_interval());

        #[cfg(feature = "metrics")]
        let metrics = config
            .serve_metrics()
            .map(|addr| crate::metrics::MetricsServer::start(*addr));
        Ok(Self {
            state,
            maintainer,
            #[cfg(feature = "metrics")]
            metrics,
        })
    }

    pub async fn shutdown(self) -> crate::Result<()> {
        let cluster_res = self.state.cluster().close().await;
        self.maintainer.stop().await;
        let snapshot_res = self.state.log().create_snapshot().await;

        #[cfg(feature = "metrics")]
        if let Some(metrics) = self.metrics {
            metrics.stop().await;
        }
        cluster_res.and(snapshot_res)
    }
}
