from typing import Dict, Any
from core.ai_engine import ai_engine
from core.logger import get_logger

logger = get_logger(__name__)


def process_summarization(task: Dict[str, Any]) -> Dict[str, Any]:
    """
    Summarizes input text using LLM
    """
    
    prompt = f"""
    Summarize the following text in a consie way:
    
    {task["input"]["text"]}
    """
    
    logger.info(f"Summarizing task {task['id']}")
    
    result = ai_engine.generate(prompt)
    
    return {
        "task_id": task["id"],
        "status": "completed",
        "result": result,
    }