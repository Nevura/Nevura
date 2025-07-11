mod pairing;
mod network;
mod update;

#[tokio::main]
async fn main() {
    pairing::init_pairing().await;
    network::configure().await;
    update::check_updates().await;
}