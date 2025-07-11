from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import libvirt
import subprocess
import xml.etree.ElementTree as ET
from ..models.vm import VM
from ..services.vm import list_vms, start_vm, stop_vm, delete_vm

router = APIRouter()

@router.get("/", response_model=list[VM])
def get_all_vms():
    return list_vms()

@router.post("/start")
def start(name: str):
    start_vm(name)
    return {"status": "started"}

@router.post("/stop")
def stop(name: str):
    stop_vm(name)
    return {"status": "stopped"}

@router.delete("/delete")
def delete(name: str):
    delete_vm(name)
    return {"status": "deleted"}

class VMInfo(BaseModel):
    uuid: str
    name: str
    state: str
    cpu: int
    memory: int
    diskCount: int

def parse_domain_disk_count(xml_desc: str) -> int:
    try:
        root = ET.fromstring(xml_desc)
        disks = root.findall(".//devices/disk[@device='disk']")
        return len(disks)
    except Exception:
        return 0

@router.get("/", response_model=List[VMInfo])
def list_vms():
    conn = libvirt.open("qemu:///system")
    if conn is None:
        return []

    vms = []
    for id in conn.listDomainsID():
        dom = conn.lookupByID(id)
        info = dom.info()
        xml_desc = dom.XMLDesc()
        vms.append(VMInfo(
            uuid=dom.UUIDString(),
            name=dom.name(),
            state=["nostate", "running", "blocked", "paused", "shutdown", "shutoff", "crashed"][info[0]] if info[0]<7 else "unknown",
            cpu=info[3],
            memory=int(info[1] / 1024),
            diskCount=parse_domain_disk_count(xml_desc)
        ))
    for name in conn.listDefinedDomains():
        dom = conn.lookupByName(name)
        info = dom.info()
        xml_desc = dom.XMLDesc()
        vms.append(VMInfo(
            uuid=dom.UUIDString(),
            name=dom.name(),
            state=["nostate", "running", "blocked", "paused", "shutdown", "shutoff", "crashed"][info[0]] if info[0]<7 else "unknown",
            cpu=info[3],
            memory=int(info[1] / 1024),
            diskCount=parse_domain_disk_count(xml_desc)
        ))

    conn.close()
    return vms

class VMCreate(BaseModel):
    name: str
    cpu: int
    memory_mb: int
    disk_gb: int
    node_id: str

class VMInfo(BaseModel):
    id: str
    name: str
    status: str
    node_id: str

vm_db = []

@router.post("/create", response_model=str)
async def create_vm(vm: VMCreate):
    # appeler système (ex: SSH au node) pour créer VM via libvirt/qemu
    vm_db.append(vm)
    return f"VM {vm.name} créée sur node {vm.node_id}"

@router.get("/", response_model=List[VMInfo])
async def list_vms():
    # récupérer VM depuis DB ou nodes
    return [
        VMInfo(id="vm1", name="Test VM", status="running", node_id="node1"),
    ]
SECRET_KEY = "CHANGE_ME_SECURE_KEY"
ALGORITHM = "HS256"

class Token(BaseModel):
    access_token: str
    token_type: str

class VMCreate(BaseModel):
    name: str
    cpu: int
    memory_mb: int
    disk_gb: int
    node_id: str

class VMInfo(BaseModel):
    uuid: str
    name: str
    state: str
    cpu: int
    memory: int
    diskCount: int
    node_id: str

@router.post("/token", response_model=Token)
def login(user = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    token = jwt.encode({
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(hours=8),
        "role": "admin"
    }, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/create", dependencies=[Depends(AdminUser)])
def create_vm(vm: VMCreate):
    # Exemple : génération XML template
    xml = f"""<domain type='kvm'><name>{vm.name}</name><vcpu>{vm.cpu}</vcpu>..."""
    conn = libvirt.open("qemu:///system")
    dom = conn.defineXML(xml)
    conn.close()
    if dom is None:
        raise HTTPException(500, "VM création échouée")
    return {"message": f"VM {vm.name} créée"}

@router.get("/", response_model=List[VMInfo])
def list_vms():
    conn = libvirt.open("qemu:///system")
    infos = []
    for id in conn.listDomainsID():
        dom = conn.lookupByID(id); i = dom.info()
        xml = dom.XMLDesc()
        count = len(ET.fromstring(xml).findall(".//devices/disk[@device='disk']"))
        infos.append(VMInfo(uuid=dom.UUIDString(), name=dom.name(),
            state="running", cpu=i[3], memory=int(i[1]/1024),
            diskCount=count, node_id="local"))
    for nm in conn.listDefinedDomains():
        dom = conn.lookupByName(nm); i = dom.info(); xml = dom.XMLDesc()
        count = len(ET.fromstring(xml).findall(".//devices/disk[@device='disk']"))
        infos.append(VMInfo(uuid=dom.UUIDString(), name=dom.name(),
            state="defined", cpu=i[3], memory=int(i[1]/1024),
            diskCount=count, node_id="local"))
    conn.close()
    return infos

@router.websocket("/console/{uuid}")
async def vm_console_ws(websocket: WebSocket, uuid: str, token: str = Depends()):
    await websocket.accept()
    # TODO : ouvrir console VNC / Spice et forward via WebSocket
    while True:
        try:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
        except WebSocketDisconnect:
            break
class ResizeInput(BaseModel):
    uuid: str
    memory_mb: int
    disk_gb: int

class SnapshotInput(BaseModel):
    uuid: str
    snapshot_name: str

class CloneInput(BaseModel):
    uuid: str
    clone_name: str

@router.post("/snapshot", dependencies=[Depends(AdminUser)])
def snapshot_vm(data: SnapshotInput):
    conn = libvirt.open("qemu:///system")
    dom = conn.lookupByUUIDString(data.uuid)
    dom.snapshotCreateXML(f"<domainsnapshot><name>{data.snapshot_name}</name></domainsnapshot>", 0)
    conn.close()
    return {"message": f"Snapshot {data.snapshot_name} created"}

@router.post("/clone", dependencies=[Depends(AdminUser)])
def clone_vm(data: CloneInput):
    conn = libvirt.open("qemu:///system")
    src = conn.lookupByUUIDString(data.uuid)
    xml = src.XMLDesc()
    tree = ET.fromstring(xml)
    tree.find("name").text = data.clone_name
    newxml = ET.tostring(tree).decode()
    dom = conn.defineXML(newxml)
    dom.create()
    conn.close()
    return {"message": f"Clone {data.clone_name} started"}

@router.post("/resize", dependencies=[Depends(AdminUser)])
def resize_vm(data: ResizeInput):
    conn = libvirt.open("qemu:///system")
    dom = conn.lookupByUUIDString(data.uuid)
    dom.setMemory(data.memory_mb * 1024)
    # Disk resize: offline or live depends on storage backend → simplified:
    disk = dom.blockInfo(dom.XMLDesc().split("<target dev='")[1].split("'")[0])
    # assume offline
    dom.destroy()
    # resize underlying image using qemu-img
    conn.close()
    return {"message": f"Resized VM {dom.name()}"}

@router.get("/{uuid}", response_model=VMDetail)
def get_vm_details(uuid: str):
    # récupère stats CPU/RAM/Disk/latence + IP/hostname/OS/focus virtio
    return VMDetail(...)

@router.post("/{uuid}/install-virtio", dependencies=[Depends(AdminUser)])
def install_virtio(uuid: str):
    # détecte OS de la VM, récupère ISO Virtio depuis serveur,
    # attache ISO au lecteur CD virtuel, démarre installation via agent
    return {"message": "Virtio ISO attachée"}
