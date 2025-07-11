import libvirt, xml.etree.ElementTree as ET
import subprocess
from ..models.vm_details import VMDetail
import socket

def get_vm_detail(uuid: str) -> VMDetail:
    conn = libvirt.open("qemu:///system")
    dom = conn.lookupByUUIDString(uuid)
    info = dom.info()
    ram_alloc_mb = int(info[1] / 1024)
    cpu_alloc = info[3]
    # CPU et RAM à partir de domain stats
    stats = dom.getCPUStats(True)[0]
    cpu_used_percent = stats['cpu_time'] / 1e9  # approximatif en seconde
    mem_stats = dom.memoryStats()
    ram_used_mb = mem_stats.get('available', 0)
    # Stockage – approximation via disk usage
    xml = dom.XMLDesc()
    tree = ET.fromstring(xml)
    disks = tree.findall(".//devices/disk[@device='disk']/target")
    disk_alloc_gb = 0.0
    disk_used_gb = 0.0
    for t in disks:
        dev = t.get('dev')
        info = conn.lookupByName(dev).blockInfo(dev)
        alloc = info[1] / (1024**3)
        disk_alloc_gb += alloc
    # latence calc via ping IP
    ip = dom.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
    ipaddr = None
    for (name, val) in ip.items():
        if val['addrs']:
            ipaddr = val['addrs'][0]['addr']
    latency_percent = 0.0
    if ipaddr:
        res = subprocess.run(["ping", "-c", "1", ipaddr], capture_output=True)
        if res.returncode == 0:
            time_ms = float(res.stdout.decode().split('time=')[1].split(' ')[0])
            latency_percent = min(time_ms / 200.0 * 100, 100.0)
    # virtio check
    virtio_installed = False
    osname = dom.OSType()
    if osname and "windows" in osname.lower():
        # detection simplifiée : recherche de pilote virtio dans guest agent
        try:
            agent = dom.QemuAgentCommand("{\"execute\":\"guest-network-get-interfaces\"}", 0, 0)
            virtio_installed = b"virtio" in agent.lower()
        except:
            virtio_installed = False
    detail = VMDetail(
        uuid=uuid,
        name=dom.name(),
        os=osname,
        ip=ipaddr,
        hostname=None,
        cpu_used_percent=cpu_used_percent,
        cpu_alloc=cpu_alloc,
        ram_used_mb=ram_used_mb,
        ram_alloc_mb=ram_alloc_mb,
        disk_used_gb=disk_used_gb,
        disk_alloc_gb=disk_alloc_gb,
        latency_percent=latency_percent,
        virtio_installed=virtio_installed
    )
    conn.close()
    return detail
