from fastapi import APIRouter
from pydantic import BaseModel
import uuid

from core.queue import task_queue
from db.job_store import save_job, get_job, update_job
from core.logger import get_logger

from rq.registry import FailedJobRegistry
from rq import Retry

router = APIRouter()

logger = get_logger(__name__)

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
    task_queue.enqueue(
        "core.tasks.process_task", 
        job_data, 
        retry=Retry(max=3, interval=[10,30,60])
    )
    
    logger.info(f"Task created: {task_id}")
    
    return job_data

@router.get("/tasks/{task_id}")
def get_task(task_id: str):
    task = get_job(task_id)
    
    if not task:
        return {"error": "Task not found"}
    
    return task
