use std::path::Path;

pub fn check() {
    println!("[Modules] Vérification des modules installés...");

    let modules = ["docker", "lxc", "qemu", "nextcloud", "ldap", "sso"];

    for module in modules.iter() {
        let path = format!("/usr/bin/{}", module);
        if Path::new(&path).exists() {
            println!("[OK] {} installé", module);
        } else {
            println!("[WARN] {} non trouvé", module);
        }
    }
}