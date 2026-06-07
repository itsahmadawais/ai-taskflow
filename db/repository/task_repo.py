from typing import Dict, Any, Optional

from sqlalchemy.orm import Session

from db.session import SessionLocal
from db.models.task import Task

def create_task(db: Session, data: Dict[str, Any]) -> Task:
    task = Task(**data)
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return task

def get_task(db: Session, task_id: str) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()

def update_task(db: Session, task_id: str, data: dict) -> Optional[Task]:
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        return None
    
    for k, v in data.items():
        setattr(task, k, v)
        
    db.commit()
    db.refresh(task)
    
    return task