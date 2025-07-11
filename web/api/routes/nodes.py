from fastapi import APIRouter, HTTPException
from typing import List
from web.api.models.nodes import Node, NodeCreate, NodeRead
from services.nodes import list_nodes, get_node, add_node, update_node, remove_node, discover_nodes

router = APIRouter()

@router.get("/", response_model=List[NodeRead])
async def get_nodes():
    return await list_nodes()

@router.get("/discover")
async def discover_network_nodes():
    nodes = await discover_nodes()
    return {"nodes": nodes}

@router.post("/", response_model=NodeRead)
async def create_node(node: NodeCreate):
    return await add_node(node)

@router.put("/{node_id}", response_model=NodeRead)
async def edit_node(node_id: int, node: NodeCreate):
    return await update_node(node_id, node)

@router.delete("/{node_id}")
async def delete_node(node_id: int):
    await remove_node(node_id)
    return {"detail": "Node deleted"}
