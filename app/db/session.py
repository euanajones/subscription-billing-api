from sqlmodel import Field, SQLModel, create_engine
from datetime import datetime

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    password_hash: str
    date_create: datetime = Field(default_factory=datetime.now)
