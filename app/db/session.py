from sqlmodel import SQLModel, Session, create_engine
from config import settings
from models import User, Organisation, OrganisationMembership, Plan

engine = create_engine(settings.DATABASE_URL, echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)

def create_users():
    user1 = User(email="tstark@email.com", password_hash="password1")
    user2 = User(email="bbanner@email.com", password_hash="password2")
    user3 = User(email="pparker@email.com", password_hash="password3")

    session = Session(engine)

    session.add(user1)
    session.add(user2)
    session.add(user3)

    session.commit()

def main():
    create_tables()
    create_users()

if __name__ == "__main__":
    main()