use reqwest;

pub async fn check_updates() {
    println!("[Tools] Vérification des mises à jour");
    match reqwest::get("https://update.nervura.io/core.json").await {
        Ok(resp) => {
            let status = resp.status();
            println!("Statut: {}", status);
        }
        Err(e) => println!("Erreur réseau: {}", e),
    }
}