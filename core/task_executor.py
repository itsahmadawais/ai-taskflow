import openai
from sqlalchemy.orm import Session

from db.session import SessionLocal
from db.repository.task_repo import get_task, update_task

from core.processors import (
    process_summarization,
    process_translation,
    process_classification,
    process_extraction,
)

PERMANENT_ERRORS = (
    openai.AuthenticationError,
    openai.PermissionDeniedError,
    openai.NotFoundError,
    openai.BadRequestError,
    ValueError,
)


def _task_payload(task) -> dict:
    return {
        "id": str(task.id),
        "task_type": task.task_type,
        "input": task.input,
    }


def execute(task_id: str):
    db: Session = SessionLocal()

    try:
        task = get_task(db, task_id)

        if not task:
            return None

        update_task(db, task_id, {"status": "processing"})

        payload = _task_payload(task)

        match task.task_type:
            case "summarize":
                result = process_summarization(payload)

            case "translate":
                result = process_translation(payload)

            case "classify":
                result = process_classification(payload)

            case "data_extraction":
                result = process_extraction(payload)

            case _:
                raise ValueError(f"Unsupported task type: {task.task_type}")

        update_task(db, task_id, {
            "status": "completed",
            "result": result["result"]
        })

        return result

    except PERMANENT_ERRORS as e:
        # Non-retryable — mark failed and do not re-raise so RQ won't retry
        update_task(db, task_id, {
            "status": "failed",
            "result": {"error": str(e)}
        })

    except Exception as e:
        # Transient error — mark failed and re-raise so RQ retries the job
        update_task(db, task_id, {
            "status": "failed",
            "result": {"error": str(e)}
        })
        raise

    finally:
        db.close()
