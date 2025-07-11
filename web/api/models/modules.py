from pydantic import BaseModel
from ..models.module import Module

class Module(BaseModel):
    id: str
    name: str
    category: str
    installed: bool
    version: str

def list_modules():
    return [
        Module(name="docker", installed=True),
        Module(name="lxc", installed=True),
        Module(name="qemu", installed=True)
    ]

def enable_module(name: str):
    pass

def disable_module(name: str):
    pass
