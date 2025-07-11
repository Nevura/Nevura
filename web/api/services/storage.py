from typing import List
from web.api.models.storages import StorageVolume, StorageCreate, StorageRead

async def list_volumes() -> List[StorageRead]:
    # Liste volumes stockages, RAID
    pass

async def get_volume(volume_id: int) -> StorageRead | None:
    # Récupère volume
    pass

async def create_volume(volume: StorageCreate) -> StorageRead:
    # Crée volume, RAID, formatage
    pass

async def delete_volume(volume_id: int) -> None:
    # Supprime volume
    pass
