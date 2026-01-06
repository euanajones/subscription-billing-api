from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

from .organisation import Organisation
from .plan import Plan

class Subscription(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    organisation_id: int = Field(foreign_key="organisation.id")
    plan_id: int = Field(foreign_key="plan.id")
    status: str
    end_date: datetime | None = None

    organisation: "Organisation" = Relationship(back_populates="organisation")
    plan: "Plan" = Relationship(back_populates="plan")