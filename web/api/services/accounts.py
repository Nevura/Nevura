from typing import List, Optional
from web.api.models.users import User, UserCreate, UserRead

async def get_users() -> List[UserRead]:
    # Récupère tous les utilisateurs
    pass

async def get_user_by_id(user_id: int) -> Optional[UserRead]:
    # Récupère utilisateur par ID
    pass

async def create_user(user: UserCreate) -> UserRead:
    # Crée un nouvel utilisateur
    pass

async def update_user(user_id: int, user: UserCreate) -> UserRead:
    # Met à jour un utilisateur
    pass

async def delete_user(user_id: int) -> None:
    # Supprime un utilisateur
    pass
