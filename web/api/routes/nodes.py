from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import datetime
import configparser
import os
import socket
import struct
import fcntl

router = APIRouter()

class NodeInfo(BaseModel):
    id: str
    name: str
    ip: str
    mac: str
    status: str
    lastSeen: str

NODE_CONF_PATH = "/etc/nervura/node.conf"

def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # connect to a public IP, doesn't send data, just to get default interface
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def get_mac_address(ip: str) -> str:
    # This is a Linux specific implementation to get MAC by IP from ARP cache
    try:
        with open("/proc/net/arp", "r") as f:
            for line in f.readlines()[1:]:
                parts = line.split()
                if parts[0] == ip:
                    return parts[3]
    except Exception:
        return ""
    return ""

def parse_nodes_conf() -> List[NodeInfo]:
    if not os.path.isfile(NODE_CONF_PATH):
        # If no config, return local node only
        local_ip = get_local_ip()
        return [
            NodeInfo(
                id="local",
                name=socket.gethostname(),
                ip=local_ip,
                mac=get_mac_address(local_ip),
                status="online",
                lastSeen=str(datetime.datetime.now())
            )
        ]
    config = configparser.ConfigParser()
    config.read(NODE_CONF_PATH)

    nodes: List[NodeInfo] = []
    for section in config.sections():
        if section.startswith("node:"):
            node_id = section[5:]
            ip = config.get(section, "ip", fallback="0.0.0.0")
            mac = config.get(section, "mac", fallback="")
            name = config.get(section, "name", fallback=f"Node {node_id}")
            status = config.get(section, "status", fallback="unknown")
            last_seen = config.get(section, "lastSeen", fallback=str(datetime.datetime.now()))
            nodes.append(NodeInfo(id=node_id, name=name, ip=ip, mac=mac, status=status, lastSeen=last_seen))

    # If no nodes found, fallback to local node only
    if len(nodes) == 0:
        local_ip = get_local_ip()
        nodes.append(NodeInfo(
            id="local",
            name=socket.gethostname(),
            ip=local_ip,
            mac=get_mac_address(local_ip),
            status="online",
            lastSeen=str(datetime.datetime.now())
        ))
    return nodes

@router.get("/", response_model=List[NodeInfo])
def list_nodes():
    return parse_nodes_conf()

@router.post("/{node_id}/wol")
def wake_on_lan_route(node_id: str):
    nodes = parse_nodes_conf()
    node = next((n for n in nodes if n.id == node_id), None)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    if not node.mac:
        raise HTTPException(status_code=400, detail="MAC address missing")
    send_wol_packet(node.mac)
    return {"message": f"WOL sent to {node.name}"}

@router.delete("/{node_id}")
def delete_node_route(node_id: str):
    nodes = parse_nodes_conf()
    nodes = [n for n in nodes if n.id != node_id]
    save_nodes_conf(nodes)
    return {"message": "Node deleted"}

@router.get("/discover")
def discover_route():
    ips = discover_nodes()
    return {"ips": [str(ip) for ip in ips]}
