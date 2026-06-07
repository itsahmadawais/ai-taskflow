from typing import Dict, Any
from core.ai_engine import ai_engine
from core.logger import get_logger

logger = get_logger(__name__)

def process_translation(task: Dict[str, Any]) -> Dict[str, Any]:
    input_data = task["input"]
    target_language = input_data.get("target_language", "en")

    prompt = f"""
    Translate the following text to {input_data["target_language"]}:
    {input_data["text"]}
    """
    
    logger.info(f"Translating task {task['id']} to {target_language}")
    
    result = ai_engine.generate(prompt)
    
    return {
        "task_id": task["id"],
        "result": result,
        "status": "completed",
    }