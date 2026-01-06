from sqlmodel import Field, SQLModel
from datetime import datetime

class Plan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float
    billing_interval_days: int
    created_at: datetime = Field(default_factory=datetime.now)