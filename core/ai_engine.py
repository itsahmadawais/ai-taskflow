from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from core.config import settings
from core.logger import get_logger

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
                f"Summarize the following text:\n\n{input}"
            )
        case "translate":
            return ChatPromptTemplate.from_template(
                f"Translate the following text to {language}:\n\n{input}"
            )
        case "classify":
            return ChatPromptTemplate.from_template(
                f"Classify the following text:\n\n{input}"
            )
        case _:
            return ChatPromptTemplate.from_template(
                f"Process the following text:\n\n{input}"
            )
            
def process_ai_task(task):
    prompt_type = task["task_type"]
    user_input = task["prompt"]
    
    logger.info(f"Processing task {task['id']} with prompt type {prompt_type}")
    
    prompt = get_prompt(prompt_type)
    
    chain = prompt | llm
    
    response = chain.invoke({
        "input": user_input
    })
    
    logger.info(f"Task {task['id']} completed successfully")
        
    return {
        "task_id": task["id"],
        "status": "completed",
        "result": response.content,
    }