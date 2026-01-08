from sqlmodel import SQLModel, Field

class Plan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float
    interval_days: int
    
    org_id: int | None = Field(default=None, foreign_key="organisation.id")