from typing import List
from web.api.models.tasks import Task, TaskCreate, TaskRead

async def list_tasks() -> List[TaskRead]:
    # Liste tâches planifiées
    pass

async def create_task(task: TaskCreate) -> TaskRead:
    # Crée tâche planifiée
    pass

async def update_task(task_id: int, task: TaskCreate) -> TaskRead:
    # Met à jour tâche
    pass

async def delete_task(task_id: int) -> None:
    # Supprime tâche
    pass
