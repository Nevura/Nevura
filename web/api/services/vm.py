from typing import List
from web.api.models.vms import VM, VMCreate, VMRead

async def list_vms() -> List[VMRead]:
    # Liste VM et containers (Docker, LXC, Jails)
    pass

async def get_vm(vm_id: int) -> VMRead | None:
    # Récupère VM par ID
    pass

async def create_vm(vm: VMCreate) -> VMRead:
    # Crée VM ou container
    pass

async def update_vm(vm_id: int, vm: VMCreate) -> VMRead:
    # Met à jour VM
    pass

async def delete_vm(vm_id: int) -> None:
    # Supprime VM
    pass
