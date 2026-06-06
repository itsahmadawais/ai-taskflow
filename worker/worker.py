import time
import json
import redis
from rq import Worker, Queue, Connection

from core.queue import redis_conn
from core.ai_engine import process_ai_task
from db.job_store import update_job

listen = ["tasks"]

def job_handler(job):
    task = json.args[0]
    job_id = task["id"]
    
    update_job(job_id, {"status": "processing"})
    
    try:
        result = process_ai_task(task)
        update_job(job_id, {
            "status": "completed", 
            "result": result["result"]
        })
        return result
    except Exception as e:
        update_job(job_id, {
            "status": "failed",
            "error": str(e)
        })
        return None

if __name__ == "__main__":
    with Connection(redis_conn):
        worker = Worker([Queue("tasks")])
        worker.work()