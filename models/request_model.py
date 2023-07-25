from typing import List
from pydantic import BaseModel
from pydantic import Field

class ChatRequest(BaseModel):
    message: str

class LLMChatRequest(BaseModel):
    query: str
    history: List[tuple]



