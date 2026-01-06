from sqlmodel import Field, SQLModel
from datetime import datetime

class OrganisationMembership(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key=True)
    org_id: int | None = Field(default=None, foreign_key=True)
    role: str