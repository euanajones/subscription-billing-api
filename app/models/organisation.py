from sqlmodel import Field, SQLModel
from datetime import datetime

class Organisation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    owner_id: int | None = Field(default=None, foreign_key=True)
    date_created: datetime = Field(default_factory=datetime.now)