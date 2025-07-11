from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import os, shutil, requests
from ..dependencies import AdminUser

ISO_DIR = "/srv/nervura/isos"

class ISOInfo(BaseModel):
    filename: str
    os: Optional[str]
    version: Optional[str]
    size: int
    added_on: str

class ISODownload(BaseModel):
    url: str
    force: Optional[bool] = False

router = APIRouter(prefix="/iso")

@router.get("/", response_model=List[ISOInfo])
def list_isos():
    if not os.path.isdir(ISO_DIR):
        os.makedirs(ISO_DIR, exist_ok=True)
    files = []
    for fn in os.listdir(ISO_DIR):
        path = os.path.join(ISO_DIR, fn)
        stats = os.stat(path)
        os_val = fn.split("_")[0] if "_" in fn else None
        version = fn.split("_")[1] if "_" in fn and "." in fn else None
        files.append(ISOInfo(
            filename=fn,
            os=os_val,
            version=version,
            size=stats.st_size,
            added_on=str(stats.st_mtime)
        ))
    return sorted(files, key=lambda x: x.added_on, reverse=True)

@router.post("/upload", dependencies=[Depends(AdminUser)])
async def upload_iso(file: UploadFile = File(...), force: bool = False):
    dest = os.path.join(ISO_DIR, file.filename)
    if os.path.exists(dest) and not force:
        raise HTTPException(status_code=409, detail="ISO already exists")
    with open(dest + ".tmp", "wb") as out:
        shutil.copyfileobj(file.file, out)
    os.replace(dest + ".tmp", dest)
    return {"message": "Uploaded"}

@router.post("/download", dependencies=[Depends(AdminUser)])
def download_iso(req: ISODownload):
    filename = req.url.split("/")[-1]
    dest = os.path.join(ISO_DIR, filename)
    if os.path.exists(dest) and not req.force:
        raise HTTPException(status_code=409, detail="ISO already exists")
    r = requests.get(req.url, stream=True)
    if r.status_code != 200:
        raise HTTPException(status_code=400, detail="Download failed")
    with open(dest, "wb") as out:
        for chunk in r.iter_content(chunk_size=8192):
            out.write(chunk)
    return {"message": "Downloaded"}

@router.delete("/{filename}", dependencies=[Depends(AdminUser)])
def delete_iso(filename: str):
    path = os.path.join(ISO_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(404, "Not found")
    os.remove(path)
    return {"message": "Deleted"}
