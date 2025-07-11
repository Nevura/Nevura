import subprocess
from ..models.vm import VM
from typing import List

def list_vms() -> List[VM]:
    return []

def start_vm(name: str):
    subprocess.run(["virsh", "start", name], check=False)

def stop_vm(name: str):
    subprocess.run(["virsh", "shutdown", name], check=False)

def delete_vm(name: str):
    subprocess.run(["virsh", "undefine", name], check=False)
