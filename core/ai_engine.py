from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from core.config import settings
from core.logger import get_logger
from core.retry import retry

import time

logger = get_logger(__name__)

llm = ChatOpenAI(
    model="gpt-4o-mini", 
    temperature=0,
    api_key=settings.OPENAI_API_KEY
)


def get_prompt(prompt_type):
    match prompt_type:
        case "summarize":
            return ChatPromptTemplate.from_template(
                "Summarize the following text:\n\n{input}"
            )
        case "translate":
            return ChatPromptTemplate.from_template(
                "Translate the following text to English:\n\n{input}"
            )
        case "classify":
            return ChatPromptTemplate.from_template(
                "Classify the following text:\n\n{input}"
            )
        case _:
            return ChatPromptTemplate.from_template(
                "Process the following text:\n\n{input}"
            )
            
def process_ai_task(task):
    start_time = time.perf_counter()
    
    prompt_type = task["task_type"]
    user_input = task["prompt"]
    
    logger.info(f"Processing task {task['id']} with prompt type {prompt_type}")
    
    prompt = get_prompt(prompt_type)
    
    chain = prompt | llm
    
    try:
        response = retry(
        lambda: chain.invoke({
            "input": user_input
        })
        )

        duration = time.perf_counter() - start_time
        logger.info(f"Task {task['id']} completed successfully in {duration:.2f} seconds")
    
        return {
            "task_id": task["id"],
            "status": "completed",
            "result": response.content,
        }
    except Exception as e:
        logger.error(f"Task {task['id']} failed: {str(e)}")
        raise