from typing import Dict, Any
from core.ai_engine import ai_engine
from core.logger import get_logger

logger = get_logger(__name__)

def process_classification(task: Dict[str, Any]) -> Dict[str, Any]:
    """
    Classifies input text using LLM
    """
    
    input_data = task["input"]
    
    categories = input_data.get("categories", [])
    
    logger.info(f"Categories: {categories}")
    
    category_instruction = (
        f"Choose one of these categories: {', '.join(categories)}."
        if categories
        else "Choose the single most appropriate category."
    )

    prompt = f"""
    Classify the following text into a single category. {category_instruction}
    Reply with the category name only — a few words, no explanation.

    Text:
    {input_data["text"]}
    """
    
    logger.info(f"Classifying task {task['id']}")
    
    result = ai_engine.generate(prompt)
    
    return {
        "task_id": task["id"],
        "result": result,
        "status": "completed",
    }