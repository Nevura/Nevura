use std::fs;

pub fn run() {
    println!("[Detect] Vérification des composants système...");

    let files = ["/etc/hostname", "/etc/nervura/nervura.conf"];

    for file in files.iter() {
        if fs::metadata(file).is_ok() {
            println!("[OK] {} trouvé", file);
        } else {
            println!("[ERR] {} manquant", file);
        }
    }
}