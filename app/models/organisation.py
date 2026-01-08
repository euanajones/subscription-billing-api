from sqlmodel import SQLModel, Field

class Organisation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str

    owner_id: int | None = Field(default=None, foreign_key="user.id")