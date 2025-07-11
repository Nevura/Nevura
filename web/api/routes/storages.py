from fastapi import APIRouter, HTTPException
from typing import List
from web.api.models.storages import StorageVolume, StorageCreate, StorageRead
from services.storage import list_volumes, get_volume, create_volume, delete_volume

router = APIRouter()

@router.get("/", response_model=List[StorageRead])
async def get_storage_volumes():
    return await list_volumes()

@router.get("/{volume_id}", response_model=StorageRead)
async def get_storage_volume(volume_id: int):
    volume = await get_volume(volume_id)
    if not volume:
        raise HTTPException(status_code=404, detail="Volume not found")
    return volume

@router.post("/", response_model=StorageRead)
async def add_storage_volume(volume: StorageCreate):
    return await create_volume(volume)

@router.delete("/{volume_id}")
async def delete_storage_volume(volume_id: int):
    await delete_volume(volume_id)
    return {"detail": "Volume deleted"}
