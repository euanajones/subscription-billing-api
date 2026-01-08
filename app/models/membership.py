from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

from .user import User
from .subscription import Subscription

class Membership(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    sub_id: int = Field(foreign_key="subscription.id")

    user: "User" = Relationship(back_populates="user")
    plan: "Subscription" = Relationship(back_populates="subscription")