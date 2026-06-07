from pydantic import BaseModel
from typing import Union, Literal, Dict, Any, Optional, List

class SummarizeInput(BaseModel):
    text: str
        
class TranslateInput(BaseModel):
    text: str
    target_language: str

class ExtractInput(BaseModel):
    text: str
    schema: Dict[str, Any]
        
class ClassifyInput(BaseModel):
    text: str
    categories: Optional[List[str]] = None
        
class TaskCreateRequest(BaseModel):
    task_type: Literal["summarize", "translate", "classify", "data_extraction"]
    input: Union[SummarizeInput, TranslateInput, ExtractInput, ClassifyInput]