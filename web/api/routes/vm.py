from fastapi import APIRouter, HTTPException
from typing import List
from web.api.models.vms import VM, VMCreate, VMRead
from services.vm import list_vms, get_vm, create_vm, update_vm, delete_vm

router = APIRouter()

@router.get("/", response_model=List[VMRead])
async def get_vms():
    return await list_vms()

@router.get("/{vm_id}", response_model=VMRead)
async def get_vm_detail(vm_id: int):
    vm = await get_vm(vm_id)
    if not vm:
        raise HTTPException(status_code=404, detail="VM not found")
    return vm

@router.post("/", response_model=VMRead)
async def add_vm(vm: VMCreate):
    return await create_vm(vm)

@router.put("/{vm_id}", response_model=VMRead)
async def edit_vm(vm_id: int, vm: VMCreate):
    return await update_vm(vm_id, vm)

@router.delete("/{vm_id}")
async def remove_vm(vm_id: int):
    await delete_vm(vm_id)
    return {"detail": "VM deleted"}
