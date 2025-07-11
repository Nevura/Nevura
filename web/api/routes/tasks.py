from fastapi import APIRouter
from typing import List
from web.api.models.tasks import Task, TaskCreate, TaskRead
from services.tasks import list_tasks, create_task, update_task, delete_task

router = APIRouter()

@router.get("/", response_model=List[TaskRead])
async def get_tasks():
    return await list_tasks()

@router.post("/", response_model=TaskRead)
async def add_task(task: TaskCreate):
    return await create_task(task)

@router.put("/{task_id}", response_model=TaskRead)
async def edit_task(task_id: int, task: TaskCreate):
    return await update_task(task_id, task)

@router.delete("/{task_id}")
async def remove_task(task_id: int):
    await delete_task(task_id)
    return {"detail": "Task deleted"}
