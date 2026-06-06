from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from core.config import settings
import os
import time

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
    
    prompt = get_prompt(prompt_type)
    
    chain = prompt | llm
    
    response = chain.invoke({
        "input": user_input
    })
        
    return {
        "task_id": task["id"],
        "status": "completed",
        "result": response.content,
    }