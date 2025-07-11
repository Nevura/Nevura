#!/usr/bin/env python3
import argparse
import subprocess
import os
import sys
import json
from pathlib import Path

BASE_CONFIG = "/etc/nervura/config.json"
LOG_PATH = "/var/log/nervura/"
MODULES_PATH = "/opt/nervura/modules/"

def handle_nodes(args):
    if args.cmd == "discover":
        output = subprocess.check_output(["ping", "-c1", "-W1", args.network + "1/24"])
        print(output.decode())
    elif args.cmd == "add":
        add_node_to_conf(args.id, args.name, args.ip, args.mac)
    elif args.cmd == "remove":
        remove_node_from_conf(args.id)
    elif args.cmd == "list":
        print_conf_nodes()

def reset_config():
    if os.path.exists(BASE_CONFIG):
        confirm = input("Confirmer la réinitialisation ? Cela effacera toute la configuration [oui/non]: ")
        if confirm.lower() == "oui":
            os.remove(BASE_CONFIG)
            print("[✔] Configuration réinitialisée.")
        else:
            print("[!] Réinitialisation annulée.")
    else:
        print("[i] Aucun fichier de configuration trouvé.")

def diagnostics():
    print("[i] Collecte des diagnostics système…")
    os.system("uptime")
    os.system("free -h")
    os.system("df -h")
    os.system("ip a")

def list_modules():
    if os.path.isdir(MODULES_PATH):
        modules = [m for m in os.listdir(MODULES_PATH) if os.path.isdir(os.path.join(MODULES_PATH, m))]
        print("Modules installés :")
        for mod in modules:
            print(f" - {mod}")
    else:
        print("[!] Aucun module trouvé.")

def restart_module(module_name):
    module_service = f"nervura-{module_name}.service"
    result = subprocess.run(["systemctl", "restart", module_service])
    if result.returncode == 0:
        print(f"[✔] Module {module_name} redémarré.")
    else:
        print(f"[✘] Échec du redémarrage de {module_name}.")

def logs(module_name=None):
    if module_name:
        log_file = Path(LOG_PATH) / f"{module_name}.log"
        if log_file.exists():
            os.system(f"less {log_file}")
        else:
            print(f"[!] Aucun journal trouvé pour le module {module_name}")
    else:
        for f in Path(LOG_PATH).glob("*.log"):
            print(f" - {f.name}")

def show_config():
    if os.path.exists(BASE_CONFIG):
        with open(BASE_CONFIG, "r") as f:
            config = json.load(f)
            print(json.dumps(config, indent=2))
    else:
        print("[!] Aucune configuration disponible.")

def parse_args():
    parser = argparse.ArgumentParser(description="NERVURA CLI – Utilitaire de gestion système.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("diagnostics", help="Afficher les diagnostics système")
    subparsers.add_parser("reset", help="Réinitialiser la configuration NERVURA")
    subparsers.add_parser("config", help="Afficher la configuration active")
    subparsers.add_parser("modules", help="Lister les modules installés")

    parser_restart = subparsers.add_parser("restart", help="Redémarrer un module")
    parser_restart.add_argument("module", help="Nom du module à redémarrer")

    parser_logs = subparsers.add_parser("logs", help="Afficher les journaux")
    parser_logs.add_argument("--module", help="Nom du module (optionnel)")

    return parser.parse_args()

def main():
    args = parse_args()

    if args.command == "diagnostics":
        diagnostics()
    elif args.command == "reset":
        reset_config()
    elif args.command == "config":
        show_config()
    elif args.command == "modules":
        list_modules()
    elif args.command == "restart":
        restart_module(args.module)
    elif args.command == "logs":
        logs(args.module)
    else:
        print("Commande invalide. Utilisez --help pour les options disponibles.")

if __name__ == "__main__":
    main()
