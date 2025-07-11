from typing import List
from web.api.models.nodes import Node, NodeCreate, NodeRead

async def list_nodes() -> List[NodeRead]:
    # Liste nodes connus
    pass

async def get_node(node_id: int) -> NodeRead | None:
    # Récupère node
    pass

async def add_node(node: NodeCreate) -> NodeRead:
    # Ajoute node (vérifie MAC/WOL)
    pass

async def update_node(node_id: int, node: NodeCreate) -> NodeRead:
    # Met à jour node
    pass

async def remove_node(node_id: int) -> None:
    # Supprime node
    pass

async def discover_nodes() -> list:
    # Scan réseau local pour nodes
    pass
