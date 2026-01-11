from fastapi import FastAPI, HTTPException, Query
from sqlmodel import SQLModel, Session, create_engine, select
from app.settings.config import settings
from app.db.models import User, UserCreate, UserPublic, UserUpdate

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
def get_users(offset: int = 0, limit: int = Query(default=30, le=100)):
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users
    
@app.get("/users/{user_id}", response_model=UserPublic)
def get_user_by_id(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        return user
    
@app.patch("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserUpdate):
    with Session(engine) as session:
        db_user = session.get(User, user_id)
        
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found.")
        
        user_data = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user
