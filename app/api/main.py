from fastapi import FastAPI, HTTPException, Query, Depends
from sqlmodel import SQLModel, Session, create_engine, select
from app.settings.config import settings
from app.db.models import User, UserCreate, UserPublic, UserUpdate

app = FastAPI()

connect_args = {"check_same_thread": False}
engine = create_engine(settings.DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def create_tables():
    SQLModel.metadata.create_all(engine)

def hash_password(password: str) -> str:
    return f"Unofficially hashed {password}"

@app.get("/health")
def health_status():
    return {"status": "ok"}

@app.on_event("startup")
def on_startup():
    create_tables()

@app.post("/users/add", response_model=UserPublic)
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    hashed_password = hash_password(user.password)
    extra_data = {"hashed_password": hashed_password}
    db_user = User.model_validate(user, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user
    
@app.get("/users", response_model=list[UserPublic])
def get_users(
    *, 
    session: Session = Depends(get_session), 
    offset: int = 0, 
    limit: int = Query(default=30, le=100)
):
    users = session.exec(select(User)).all()
    return users
    
@app.get("/users/{user_id}", response_model=UserPublic)
def get_user_by_id(*, session: Session = Depends(get_session) ,user_id: int):
    user = session.get(User, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user
    
@app.patch("/users/{user_id}", response_model=UserPublic)
def update_user(*, session: Session = Depends(get_session) ,user_id: int, user: UserUpdate):
    db_user = session.get(User, user_id)
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    user_data = user.model_dump(exclude_unset=True)

    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = hash_password(password)
        extra_data["hashed_password"] = hashed_password

    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@app.delete("/users/{user_id}")
def delete_user_by_id(*, session: Session = Depends(get_session) ,user_id: int):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    session.delete(user)
    session.commit()
    return {"User: {user_id} - Deleted": True}