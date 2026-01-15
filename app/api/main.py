from fastapi import FastAPI
from sqlmodel import SQLModel, Session, create_engine
from app.settings.config import settings
import bcrypt

app = FastAPI()

connect_args = {"check_same_thread": False}
engine = create_engine(settings.DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_tables():
    SQLModel.metadata.create_all(engine)

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)

    return hashed_password

@app.get("/health")
def health_status():
    return {"status": "ok"}

@app.on_event("startup")
def on_startup():
    create_tables()
