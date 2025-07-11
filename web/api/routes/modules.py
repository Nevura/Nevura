from fastapi import APIRouter, HTTPException
from typing import List
from web.api.models.modules import Module, ModuleCreate, ModuleRead
from services.modules import list_modules, get_module, install_module, uninstall_module

router = APIRouter()

@router.get("/", response_model=List[ModuleRead])
async def get_modules():
    return await list_modules()

@router.get("/{module_id}", response_model=ModuleRead)
async def get_module_detail(module_id: int):
    module = await get_module(module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module

@router.post("/install")
async def install_module_route(module: ModuleCreate):
    await install_module(module)
    return {"detail": "Module installation started"}

@router.post("/uninstall/{module_id}")
async def uninstall_module_route(module_id: int):
    await uninstall_module(module_id)
    return {"detail": "Module uninstallation started"}
