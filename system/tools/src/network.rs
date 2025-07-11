use std::process::Command;

pub async fn configure() {
    println!("[Tools] Configuration réseau");
    if let Ok(output) = Command::new("ip").arg("addr").output() {
        println!("{}", String::from_utf8_lossy(&output.stdout));
    }
}