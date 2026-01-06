from sqlmodel import Field, SQLModel
from datetime import datetime

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    password_hash: str
    date_created: datetime = Field(default_factory=datetime.now)