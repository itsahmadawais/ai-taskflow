import json
from core.queue import redis_conn

JOB_PREFIX = "job:"

def save_job(job_id, job_data):
    redis_conn.set(JOB_PREFIX + job_id, json.dumps(job_data))
    
def get_job(job_id):
    job_data = redis_conn.get(JOB_PREFIX + job_id)
    if job_data:
        return json.loads(job_data)
    return None
    
def update_job(job_id, job_data):
    job = get_job(job_id)
    
    if not job_data:
        return None
    
    job.update(job_data)
    redis_conn.set(JOB_PREFIX + job_id, json.dumps(job))
    return job