from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str
    password: str

    organisations: list["Organisation"] = Relationship(back_populates="owner")

class Organisation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    owner_id: int = Field(default=None, foreign_key="user.id", ondelete="SET NULL")
    owner: User = Relationship(back_populates="organisations")

    plans: list["Plan"] = Relationship(back_populates="organisation_owner", cascade_delete=True)

class Plan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float
    interval_days: int
    
    org_id: int | None = Field(default=None, foreign_key="organisation.id", ondelete="CASCADE")
    organisation_owner: Organisation = Relationship(back_populates="plans")

class Subscription(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    user_id: int | None = Field(default=None, foreign_key="user.id")
    plan_id: int | None = Field(default=None, foreign_key="plan.id")

    start_date: datetime
    end_date: datetime