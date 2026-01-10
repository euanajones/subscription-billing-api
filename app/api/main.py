from fastapi import FastAPI
from sqlmodel import SQLModel, Session, create_engine, select
from app.settings.config import settings
from app.db.models import User

app = FastAPI()

connect_args = {"check_same_thread": False}
engine = create_engine(settings.DATABASE_URL, echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)

@app.get("/health")
def health_status():
    return {"status": "ok"}

@app.on_event("startup")
def on_startup():
    create_tables()

@app.post("/users/add")
def create_user(user: User):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    
@app.get("/users")
def get_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users