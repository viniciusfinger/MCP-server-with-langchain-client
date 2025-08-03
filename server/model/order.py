from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from decimal import Decimal


class Order(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: int
    customer_id: int = Field(alias="customerId")
    customer_name: str = Field(alias="customerName")
    date: datetime
    amount: Decimal