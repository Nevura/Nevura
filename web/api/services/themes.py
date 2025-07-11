from typing import List
from web.api.models.themes import Theme, ThemeCreate, ThemeRead

async def list_themes() -> List[ThemeRead]:
    # Liste thèmes disponibles
    pass

async def create_theme(theme: ThemeCreate) -> ThemeRead:
    # Ajoute un thème
    pass

async def apply_theme(theme_id: int) -> None:
    # Applique un thème
    pass
