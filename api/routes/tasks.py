from fastapi import APIRouter, HTTPException
from fastapi import Depends

from sqlalchemy.orm import Session
from db.dependencies import get_db

from schemas.task_schema import TaskCreateRequest

from db.repository.task_repo import create_task as db_create_task, get_task as db_get_task

from core.queue import task_queue
from core.logger import get_logger

from rq import Retry

router = APIRouter()

logger = get_logger(__name__)

@router.post("/tasks")
def create_task(task: TaskCreateRequest, db: Session = Depends(get_db)):

    task_data = {
        "task_type": task.task_type,
        "input": task.input.model_dump(),
        "status": "pending",
    }
    
    db_task = db_create_task(db, task_data)
    task_id = str(db_task.id)
    
    task_queue.enqueue(
        "core.task_executor.execute",
        task_id,
        retry=Retry(max=3, interval=[10, 30, 60])
    )
    
    logger.info(f"Task created: {task_id}")
    
    return {
        "id": task_id,
        "task_type": task.task_type,
        "status": db_task.status,
        "input": db_task.input,
    }

@router.get("/tasks/{task_id}")
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = db_get_task(db, task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task
