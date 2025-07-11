from fastapi import APIRouter
from ..services.certs import list_certs
from ..models.cert import Cert

router = APIRouter()

@router.get("/", response_model=list[Cert])
def get_certs():
    return list_certs()
