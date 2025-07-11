use clap::{Subcommand, Args};
use std::{fs, process::Command};
use serde::{Deserialize, Serialize};

#[derive(Subcommand)]
pub enum NodeCommands {
    Add(NodeAddArgs),
    Remove(NodeRemoveArgs),
    List,
    Discover,
}

#[derive(Args)]
pub struct NodeAddArgs {
    pub id: String,
    pub name: String,
    pub ip: String,
    pub mac: String,
}

#[derive(Args)]
pub struct NodeRemoveArgs {
    pub id: String,
}

#[derive(Serialize, Deserialize)]
struct Node {
    id: String,
    name: String,
    ip: String,
    mac: String,
    status: String,
    last_seen: String,
}

pub fn handle(cmd: NodeCommands) {
    let path = "/etc/nervura/node.conf";
    let content = fs::read_to_string(path).unwrap_or("[]".into());
    let mut nodes: Vec<Node> = serde_json::from_str(&content).unwrap_or_default();

    match cmd {
        NodeCommands::Add(args) => {
            if nodes.iter().any(|n| n.id == args.id) {
                println!("Node already exists");
                return;
            }
            let node = Node {
                id: args.id,
                name: args.name,
                ip: args.ip,
                mac: args.mac,
                status: "online".into(),
                last_seen: chrono::Utc::now().to_rfc3339(),
            };
            nodes.push(node);
            fs::write(path, serde_json::to_string_pretty(&nodes).unwrap()).unwrap();
            println!("Node added.");
        }
        NodeCommands::Remove(args) => {
            nodes.retain(|n| n.id != args.id);
            fs::write(path, serde_json::to_string_pretty(&nodes).unwrap()).unwrap();
            println!("Node removed.");
        }
        NodeCommands::List => {
            for node in &nodes {
                println!("{} ({}) - {} - {}", node.name, node.id, node.ip, node.status);
            }
        }
        NodeCommands::Discover => {
            for i in 1..=254 {
                let ip = format!("192.168.1.{}", i);
                let out = Command::new("ping").arg("-c1").arg("-W1").arg(&ip).output();
                if let Ok(o) = out {
                    if o.status.success() {
                        println!("Detected: {}", ip);
                    }
                }
            }
        }
    }
}
