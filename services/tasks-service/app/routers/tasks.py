from fastapi import APIRouter

router = APIRouter()

FAKE_TASKS = [
    {"id": 1, "title": "Test task", "completed": False}
]

@router.get("/")
async def list_tasks():
    return FAKE_TASKS

@router.post("/")
async def create_task(task: dict):
    task["id"] = len(FAKE_TASKS) + 1
    FAKE_TASKS.append(task)
    return task
