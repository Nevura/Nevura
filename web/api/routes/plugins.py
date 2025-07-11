from fastapi import APIRouter, HTTPException
from typing import List
from web.api.models.plugins import Plugin, PluginCreate, PluginRead
from services.plugins import list_plugins, install_plugin, uninstall_plugin

router = APIRouter()

@router.get("/", response_model=List[PluginRead])
async def get_plugins():
    return await list_plugins()

@router.post("/install")
async def install_plugin_route(plugin: PluginCreate):
    await install_plugin(plugin)
    return {"detail": "Plugin installation started"}

@router.post("/uninstall/{plugin_id}")
async def uninstall_plugin_route(plugin_id: int):
    await uninstall_plugin(plugin_id)
    return {"detail": "Plugin uninstallation started"}
