from typing import List
from pydantic import BaseModel
from pydantic import Field

class ChatResponse(BaseModel):
    reply: str

class LLMChatResponse(BaseModel):
    response: str
    history: List[tuple]



