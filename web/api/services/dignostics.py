import psutil
from ..models.diagnostics import Diagnostics

def get_diagnostics() -> Diagnostics:
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    load = psutil.getloadavg()[0]
    return Diagnostics(
        cpu_load=load,
        memory_used=mem.used,
        memory_total=mem.total,
        disk_used=disk.used,
        disk_total=disk.total
    )
