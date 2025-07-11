from fastapi import APIRouter, HTTPException
from typing import List
from web.api.models.shares import Share, ShareCreate, ShareRead
from services.shares import list_shares, get_share, create_share, update_share, delete_share

router = APIRouter()

@router.get("/", response_model=List[ShareRead])
async def get_shares():
    return await list_shares()

@router.get("/{share_id}", response_model=ShareRead)
async def get_share_detail(share_id: int):
    share = await get_share(share_id)
    if not share:
        raise HTTPException(status_code=404, detail="Share not found")
    return share

@router.post("/", response_model=ShareRead)
async def add_share(share: ShareCreate):
    return await create_share(share)

@router.put("/{share_id}", response_model=ShareRead)
async def edit_share(share_id: int, share: ShareCreate):
    return await update_share(share_id, share)

@router.delete("/{share_id}")
async def remove_share(share_id: int):
    await delete_share(share_id)
    return {"detail": "Share deleted"}
