from pydantic import BaseModel

class ChatInput(BaseModel):
    thread_id: str
    question: str