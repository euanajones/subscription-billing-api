from sqlmodel import SQLModel, Session, create_engine, select, or_, col
from app.settings.config import settings
from typing import Annotated
from models import User
from fastapi import Depends

engine = create_engine(settings.DATABASE_URL, echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)

def create_users():
    user1 = User(email="tstark@email.com", password_hash="password1")
    user2 = User(email="bbanner@email.com", password_hash="password2")
    user3 = User(email="pparker@email.com", password_hash="password3")

    with Session(engine) as session:
        session.add(user1)
        session.add(user2)
        session.add(user3)

        session.commit()
        session.refresh()

def fetch_users():
    with Session(engine) as session:
        selection = select(User)
        results = session.exec(selection)
        users = results.all()
        
        for user in results:
            print(user)

        print(users)

def fetch_user2():
    with Session(engine) as session:
        selection = select(User).where(col(User.id) == 2)
        results = session.exec(selection)
        user = results.all()

        print(user)

def main():
    create_tables()
    create_users()
    fetch_users()

def create_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(create_session)]

if __name__ == "__main__":
    main()