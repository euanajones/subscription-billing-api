from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: str

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field()

    # 1 User : N Organisations
    organisations: None | list["Organisation"] = Relationship(back_populates="owner")

    # 1 User : N Subscriptions
    subscriptions: None | list["Subscription"] = Relationship(back_populates="user", cascade_delete=True)

class UserCreate(UserBase):
    password: str

class UserPublic(UserBase):
    id: int

class UserUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    password: str | None = None

class OrganisationBase(SQLModel):
    name: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", ondelete="SET NULL")

class Organisation(OrganisationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    
    # 1 Organisation : 1 User
    owner: User = Relationship(back_populates="organisations")

    # 1 Organisation : N Plans
    plans: list["Plan"] = Relationship(back_populates="organisation_owner", cascade_delete=True)

class OrganisationCreate(OrganisationBase):
    pass

class OrganisationPublic(OrganisationBase):
    id: int

class OrganisationUpdate(SQLModel):
    name: str | None = None

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