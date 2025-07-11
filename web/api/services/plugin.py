from typing import List
from web.api.models.plugins import Plugin, PluginCreate, PluginRead

async def list_plugins() -> List[PluginRead]:
    # Liste plugins installés
    pass

async def install_plugin(plugin: PluginCreate) -> None:
    # Installe plugin
    pass

async def uninstall_plugin(plugin_id: int) -> None:
    # Désinstalle plugin
    pass
