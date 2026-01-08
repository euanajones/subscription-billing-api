from sqlmodel import SQLModel, Field, Relationship
from .organisation import Organisation

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str
    password: str

    organisations: list["Organisation"] = Relationship(back_populates="user")