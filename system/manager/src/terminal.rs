use axum::{
    extract::ws::{Message, WebSocket, WebSocketUpgrade},
    response::IntoResponse,
    routing::get,
    Router,
};
use futures::{sink::SinkExt, stream::StreamExt};
use tokio::process::{Command, ChildStdin, ChildStdout};
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use std::sync::Arc;
use tokio::sync::Mutex;

pub async fn terminal_ws(ws: WebSocketUpgrade) -> impl IntoResponse {
    ws.on_upgrade(handle_socket)
}

async fn handle_socket(mut socket: WebSocket) {
    // For demo, launch local shell (in real, launch SSH to node IP)
    let mut child = Command::new("bash")
        .stdin(std::process::Stdio::piped())
        .stdout(std::process::Stdio::piped())
        .spawn()
        .expect("failed to spawn shell");

    let mut stdin = child.stdin.take().unwrap();
    let mut stdout = child.stdout.take().unwrap();

    // Forward from shell stdout to websocket
    let mut stdout_buf = [0u8; 1024];
    let socket_send = Arc::new(Mutex::new(socket));

    let socket_send_clone = socket_send.clone();
    tokio::spawn(async move {
        loop {
            let n = match stdout.read(&mut stdout_buf).await {
                Ok(n) if n == 0 => break,
                Ok(n) => n,
                Err(_) => break,
            };
            let text = String::from_utf8_lossy(&stdout_buf[..n]).to_string();
            let mut socket = socket_send_clone.lock().await;
            if socket.send(Message::Text(text)).await.is_err() {
                break;
            }
        }
    });

    // Forward from websocket to shell stdin
    while let Some(Ok(msg)) = socket_send.lock().await.next().await {
        if let Message::Text(text) = msg {
            if stdin.write_all(text.as_bytes()).await.is_err() {
                break;
            }
        }
    }

    let _ = child.wait().await;
}
