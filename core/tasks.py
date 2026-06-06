from db.job_store import update_job
import time

def process_task(job_data):
    print("WORKER EXECUTING:", job_data["id"])

    update_job(job_data["id"], {
        "status": "processing"
    })

    time.sleep(2)

    update_job(job_data["id"], {
        "status": "completed",
        "result": f"Processed: {job_data['prompt']}"
    })