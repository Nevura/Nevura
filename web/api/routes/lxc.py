from fastapi import APIRouter
from ..services.container import list_containers
from ..models.container import Container

router = APIRouter()

@router.get("/", response_model=list[Container])
def get_all_lxc():
    return list_containers()
