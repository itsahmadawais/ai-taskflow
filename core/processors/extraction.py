import json
from typing import Dict, Any

from core.ai_engine import ai_engine
from core.logger import get_logger

logger = get_logger(__name__)


def process_extraction(task: Dict[str, Any]) -> Dict[str, Any]:
    input_data = task["input"]
    text = input_data["text"]
    schema = input_data.get("schema", {})

    prompt = f"""
    Extract structured data from the following text using this schema:
    {json.dumps(schema)}

    Text:
    {text}

    Return valid JSON only.
    """

    logger.info(f"Extracting data for task {task['id']}")

    result = ai_engine.generate(prompt)

    return {
        "task_id": task["id"],
        "status": "completed",
        "result": result,
    }
