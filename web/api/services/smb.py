import subprocess

async def create_smb_share(name: str, path: str, options: dict) -> None:
    # Crée un partage Samba (modifie smb.conf puis reload service)
    pass

async def remove_smb_share(name: str) -> None:
    # Supprime un partage Samba
    pass

async def list_smb_shares() -> list:
    # Liste partages SMB actifs
    pass
