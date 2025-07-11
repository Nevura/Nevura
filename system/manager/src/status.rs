use std::process::Command;

pub fn print() {
    println!("[Status] Informations système :");

    if let Ok(output) = Command::new("hostnamectl").output() {
        println!("{}", String::from_utf8_lossy(&output.stdout));
    }
}