from fastapi import APIRouter
from ..services.network import get_network_interfaces
from ..models.network import NetworkInterface

router = APIRouter()

@router.get("/", response_model=list[NetworkInterface])
def interfaces():
    return get_network_interfaces()
