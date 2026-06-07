import time
from core.logger import get_logger

logger = get_logger(__name__)


def retry(fn, retries=3, delay=2):
    for attempt in range(retries):
        try:
            return fn()
        except Exception as e:
            logger.warning(f"Attempt {attempt+1} failed: {str(e)}")
            
            if attempt == retries -1:
                raise
            
            time.sleep(delay * (attempt + 1))
            