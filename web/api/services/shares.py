from typing import List
from web.api.models.shares import Share, ShareCreate, ShareRead

async def list_shares() -> List[ShareRead]:
    # Liste partages SMB, FTP, NFS
    pass

async def get_share(share_id: int) -> ShareRead | None:
    # Récupère partage
    pass

async def create_share(share: ShareCreate) -> ShareRead:
    # Crée partage SMB, FTP, NFS
    pass

async def update_share(share_id: int, share: ShareCreate) -> ShareRead:
    # Met à jour partage
    pass

async def delete_share(share_id: int) -> None:
    # Supprime partage
    pass
