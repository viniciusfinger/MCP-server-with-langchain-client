from pydantic import BaseModel

class ChatOutput(BaseModel):
    answer: str