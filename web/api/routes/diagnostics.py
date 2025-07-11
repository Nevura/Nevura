from fastapi import APIRouter
from services.diagnostics import run_diagnostics

router = APIRouter()

@router.get("/")
async def diagnostics():
    results = await run_diagnostics()
    return results
