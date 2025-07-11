from fastapi import APIRouter, HTTPException, Depends
from typing import List
from web.api.models.users import User, UserCreate, UserRead
from services.accounts import (
    get_users, get_user_by_id, create_user, update_user, delete_user
)

router = APIRouter()

@router.get("/", response_model=List[UserRead])
async def list_accounts():
    return await get_users()

@router.get("/{user_id}", response_model=UserRead)
async def get_account(user_id: int):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserRead)
async def add_account(user: UserCreate):
    return await create_user(user)

@router.put("/{user_id}", response_model=UserRead)
async def edit_account(user_id: int, user: UserCreate):
    return await update_user(user_id, user)

@router.delete("/{user_id}")
async def remove_account(user_id: int):
    await delete_user(user_id)
    return {"detail": "User deleted"}
