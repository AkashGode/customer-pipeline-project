from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


class CustomerSchema(BaseModel):
    customer_id: str
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[str] = None
    account_balance: Optional[float] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True
