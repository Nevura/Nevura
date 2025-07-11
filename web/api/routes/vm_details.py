from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..models.vm_details import VMDetail
from ..services.vm_details import get_vm_detail
from ..dependencies import AdminUser

router = APIRouter(prefix="/vm")

@router.get("/{uuid}", response_model=VMDetail)
def vm_detail(uuid: str):
    try:
        return get_vm_detail(uuid)
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@router.post("/{uuid}/install-virtio", dependencies=[Depends(AdminUser)])
def install_virtio(uuid: str):
    # Implémenter l’attachement ISO virtio
    return {"message": "Virtio ISO attached for install"}
