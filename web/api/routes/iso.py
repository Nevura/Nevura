from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from web.api.models.iso import ISOInfo
from services.iso import list_isos, upload_iso, download_iso_from_url, download_iso_from_ftp_smb_ssh

router = APIRouter()

@router.get("/", response_model=List[ISOInfo])
async def get_isos():
    return await list_isos()

@router.post("/upload")
async def upload_iso_route(file: UploadFile = File(...)):
    await upload_iso(file)
    return {"detail": "ISO uploaded"}

@router.post("/download")
async def download_iso_route(url: str):
    await download_iso_from_url(url)
    return {"detail": "ISO download started"}

@router.post("/download/ftp_smb_ssh")
async def download_iso_ftp_smb_ssh_route(url: str, protocol: str):
    await download_iso_from_ftp_smb_ssh(url, protocol)
    return {"detail": f"ISO download via {protocol} started"}
