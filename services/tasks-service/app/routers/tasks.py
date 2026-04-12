from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_user_id
from app.services.task import TaskService
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()

@router.get("/", response_model=list[TaskResponse])
async def list_tasks(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await TaskService(db).get_all(user_id)

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task(
    data: TaskCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await TaskService(db).create(user_id=user_id, title=data.title, description=data.description)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await TaskService(db).get_by_id(task_id, user_id)

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    data: TaskUpdate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    return await TaskService(db).update(
        task_id, user_id,
        title=data.title,
        description=data.description,
        is_done=data.is_done,
    )

@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    await TaskService(db).delete(task_id, user_id)
