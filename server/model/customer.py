from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class Customer(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: int
    name: str
    country: str
    joined_at: datetime = Field(alias="joinedAt")
