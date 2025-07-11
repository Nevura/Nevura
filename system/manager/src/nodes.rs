use axum::{Json, extract::Path, routing::{get, post, delete}, Router, http::StatusCode};
use serde::{Deserialize, Serialize};
use std::{fs, net::IpAddr, collections::HashSet};
use std::sync::{Arc, Mutex};
use std::process::Command;

#[derive(Serialize, Deserialize, Clone)]
pub struct Node {
    pub id: String,
    pub name: String,
    pub ip: String,
    pub mac: String,
    pub status: String,
    pub last_seen: String,
}

#[derive(Clone)]
pub struct AppState {
    pub nodes: Arc<Mutex<Vec<Node>>>,
}

#[derive(Deserialize)]
pub struct NodeInput {
    pub id: String,
    pub name: String,
    pub ip: String,
    pub mac: String,
}

pub fn router() -> Router {
    Router::new()
        .route("/nodes", get(list_nodes).post(add_node))
        .route("/nodes/discover", get(discover_nodes))
        .route("/nodes/:id", delete(delete_node))
}

async fn list_nodes(state: axum::extract::Extension<AppState>) -> Json<Vec<Node>> {
    let nodes = state.nodes.lock().unwrap();
    Json(nodes.clone())
}

async fn add_node(
    Json(payload): Json<NodeInput>,
    state: axum::extract::Extension<AppState>,
) -> StatusCode {
    let mut nodes = state.nodes.lock().unwrap();
    if nodes.iter().any(|n| n.id == payload.id) {
        return StatusCode::CONFLICT;
    }
    nodes.push(Node {
        id: payload.id.clone(),
        name: payload.name,
        ip: payload.ip,
        mac: payload.mac,
        status: "online".into(),
        last_seen: chrono::Utc::now().to_rfc3339(),
    });
    save_nodes(&nodes);
    StatusCode::CREATED
}

async fn delete_node(
    Path(id): Path<String>,
    state: axum::extract::Extension<AppState>,
) -> StatusCode {
    let mut nodes = state.nodes.lock().unwrap();
    nodes.retain(|n| n.id != id);
    save_nodes(&nodes);
    StatusCode::NO_CONTENT
}

async fn discover_nodes() -> Json<Vec<IpAddr>> {
    let mut found = HashSet::new();
    for i in 1..=254 {
        let ip = format!("192.168.1.{}", i);
        let ping = Command::new("ping")
            .arg("-c1")
            .arg("-W1")
            .arg(&ip)
            .output();

        if let Ok(p) = ping {
            if p.status.success() {
                if let Ok(ip_parsed) = ip.parse() {
                    found.insert(ip_parsed);
                }
            }
        }
    }
    Json(found.into_iter().collect())
}

fn save_nodes(nodes: &[Node]) {
    let conf = serde_json::to_string_pretty(nodes).unwrap();
    fs::write("/etc/nervura/node.conf", conf).unwrap_or_else(|_| ());
}
