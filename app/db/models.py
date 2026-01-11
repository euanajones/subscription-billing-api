from sqlmodel import SQLModel, Field, Relationship, create_engine
from datetime import datetime

class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: str

    # 1 User : N Organisations
    organisations: None | list["Organisation"] = Relationship(back_populates="owner")

    # 1 User : N Subscriptions
    subscriptions: None | list["Subscription"] = Relationship(back_populates="user", cascade_delete=True)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class UserCreate(UserBase):
    pass

class UserPublic(UserBase):
    id: int

class Organisation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    owner_id: int | None = Field(default=None, foreign_key="user.id", ondelete="SET NULL")
    # 1 Organisation : 1 User
    owner: User = Relationship(back_populates="organisations")

    # 1 Organisation : N Plans
    plans: list["Plan"] = Relationship(back_populates="organisation_owner", cascade_delete=True)

class Plan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float
    interval_days: int
    
    org_id: int | None = Field(default=None, foreign_key="organisation.id", ondelete="CASCADE")
    # 1 Plan : 1 Organisation
    organisation_owner: Organisation = Relationship(back_populates="plans")

    # 1 Plan : N Subscriptions
    subscriptions: list["Subscription"] = Relationship(back_populates="plan", cascade_delete=True)

class Subscription(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    user_id: int | None = Field(default=None, foreign_key="user.id", ondelete="CASCADE")
    # 1 Subscription : 1 User
    user: User = Relationship(back_populates="subscriptions")

    plan_id: int | None = Field(default=None, foreign_key="plan.id", ondelete="CASCADE")
    # 1 Subscription : 1 Plan
    plan: Plan = Relationship(back_populates="subscriptions")

    start_date: datetime
    end_date: datetime