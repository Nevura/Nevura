mod detect;
mod status;
mod modules;

fn main() {
    println!("[NERVURA] Initialisation du système...");
    detect::run();
    status::print();
    modules::check();
}

use axum::{Router, Extension};
use std::sync::Arc;
use tokio::sync::Mutex;

mod nodes;
mod terminal;

#[tokio::main]
async fn main() {
    let app_state = Arc::new(nodes::AppState {
        nodes: Mutex::new(vec![]),
    });

    let app = Router::new()
        .merge(nodes::router())
        .route("/ws/terminal", axum::routing::get(terminal::terminal_ws))
        .layer(Extension(app_state));

    axum::Server::bind(&"0.0.0.0:3000".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}
