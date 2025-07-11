from typing import List
from web.api.models.modules import Module, ModuleCreate, ModuleRead

async def list_modules() -> List[ModuleRead]:
    # Liste tous les modules installés
    pass

async def get_module(module_id: int) -> ModuleRead | None:
    # Récupère un module
    pass

async def install_module(module: ModuleCreate) -> None:
    # Lance installation module
    pass

async def uninstall_module(module_id: int) -> None:
    # Désinstalle module
    pass
