from fastapi import UploadFile
import aiofiles

async def list_isos() -> list:
    # Liste fichiers ISO disponibles
    return []

async def upload_iso(file: UploadFile) -> None:
    # Sauvegarde ISO uploadé localement
    async with aiofiles.open(f"/isos/{file.filename}", 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

async def download_iso_from_url(url: str) -> None:
    # Télécharge ISO depuis HTTP/HTTPS
    pass

async def download_iso_from_ftp_smb_ssh(url: str, protocol: str) -> None:
    # Télécharge ISO via FTP, SMB ou SSH
    pass
