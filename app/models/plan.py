from sqlmodel import Field, SQLModel
from datetime import datetime

class Plan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float
    interval_days: int
    date_created: datetime = Field(default_factory=datetime.now)