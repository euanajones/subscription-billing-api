from sqlmodel import SQLModel, create_engine
from config import settings
from models import User, Organisation, OrganisationMembership, Plan

engine = create_engine(settings.DATABASE_URL, echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_tables()