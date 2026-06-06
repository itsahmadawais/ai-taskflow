from fastapi import APIRouter
from pydantic import BaseModel
import uuid

from core.queue import task_queue
from core.tasks import process_task
from db.job_store import save_job, get_job, update_job

router = APIRouter()

class TaskRequest(BaseModel):
    prompt: str
    task_type: str = "summarize"

@router.post("/tasks")
def create_task(task: TaskRequest):
    task_id = str(uuid.uuid4())
    
    job_data = {
        "id": task_id,
        "prompt": task.prompt,
        "task_type": task.task_type,
        "status": "pending",
        "result": None,
    }
    
    save_job(task_id, job_data)
    task_queue.enqueue("core.tasks.process_task", job_data)
    
    return job_data

@router.get("/tasks/{task_id}")
def get_task(task_id: str):
    task = get_job(task_id)
    
    if not task:
        return {"error": "Task not found"}
    
    return task