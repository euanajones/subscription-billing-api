from sqlmodel import SQLModel, Field
from datetime import datetime

class Subscription(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    user_id: int | None = Field(default=None, foreign_key="user.id")
    plan_id: int | None = Field(default=None, foreign_key="plan.id")

    start_date: datetime
    end_date: datetime