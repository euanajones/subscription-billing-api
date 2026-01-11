from fastapi import FastAPI
from sqlmodel import SQLModel, Session, create_engine, select
from app.settings.config import settings
from app.db.models import User, UserCreate, UserPublic

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

@app.post("/users/add", response_model=UserPublic)
def create_user(user: UserCreate):
    with Session(engine) as session:
        db_user = User.model_validate(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    
@app.get("/users", response_model=list[UserPublic])
def get_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users