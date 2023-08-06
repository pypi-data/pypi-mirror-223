use super::METRICS;
use prometheus_client::encoding::text::encode;
use std::io;
use std::{net::SocketAddr, sync::Arc};

use hyper::service::{make_service_fn, service_fn};
use tokio::{sync::Notify, task::JoinHandle};

#[derive(Debug)]
pub struct MetricsServer {
    handle: JoinHandle<()>,
    stop: Arc<Notify>,
}

impl MetricsServer {
    pub fn start(address: SocketAddr) -> Self {
        let stop = Arc::new(Notify::new());
        let run_stop = stop.clone();
        let handle = tokio::spawn(Self::run(address, run_stop));
        Self { handle, stop }
    }

    pub async fn stop(self) {
        self.stop.notify_one();
        if let Err(error) = self.handle.await {
            tracing::error!(?error, "metrics server panicked");
        }
    }

    async fn run(address: SocketAddr, stop: Arc<Notify>) {
        hyper::Server::bind(&address)
            .serve(make_service_fn(move |_conn| async move {
                Ok::<_, io::Error>(service_fn(|_req| async move {
                    let mut buf = String::new();
                    encode(&mut buf, &METRICS.lock().unwrap())
                        .map_err(|e| io::Error::new(io::ErrorKind::Other, e))
                        .map(|_| {
                            let body = hyper::Body::from(buf);
                            hyper::Response::builder()
                                .header(
                                    hyper::header::CONTENT_TYPE,
                                    "application/openmetrics-text; version=1.0.0; charset=utf-8",
                                )
                                .body(body)
                                .unwrap()
                        })
                }))
            }))
            .with_graceful_shutdown(async move {
                stop.notified().await;
            })
            .await
            .unwrap();
    }
}
