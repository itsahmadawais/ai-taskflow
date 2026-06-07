from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from core.config import settings
from core.logger import get_logger
from core.retry import retry

import time

logger = get_logger(__name__)

class AIEngine:
    """
    Single entry point for all LLM interactions.
    Keeps model config centralized.
    """
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            api_key=settings.OPENAI_API_KEY
        )
        
    def generate(self, prompt: str) -> str:
        start_time = time.perf_counter()
               
        try:
            response = retry(
                lambda: self.llm.invoke(prompt)
            )
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise
        
        duration = time.perf_counter() - start_time
        logger.info(f"Response generated in {duration:.2f} seconds")
        
        return response.content
        
ai_engine = AIEngine()