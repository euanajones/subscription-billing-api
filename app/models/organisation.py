from sqlmodel import SQLModel, Field, Relationship
from .user import User

class Organisation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    owner_id: int = Field(default=None, foreign_key="user.id")
    owner: User = Relationship(back_populates="organisations")