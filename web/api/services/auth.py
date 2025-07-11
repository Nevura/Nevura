from web.api.models.users import UserRead

async def authenticate_user(username: str, password: str) -> UserRead | None:
    # Authentifie user, retourne UserRead ou None
    pass

async def create_access_token(user: UserRead) -> str:
    # Crée token JWT sécurisé
    pass

async def get_current_user() -> UserRead:
    # Récupère user depuis token d'authentification
    pass

async def revoke_tokens_for_user(user_id: int) -> None:
    # Révoque tokens
    pass

async def detect_token_anomaly(request, user: UserRead) -> bool:
    # Détecte anomalie token (IP, user agent, etc.)
    pass
