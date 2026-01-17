from fastapi import HTTPException, Query, Depends
from sqlmodel import Session, select
from db import *
from main import app, get_session, hash_password

@app.post("/users/create", response_model=UserPublic)
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
def delete_user_by_id(*, session: Session = Depends(get_session), user_id: int):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    session.delete(user)
    session.commit()
    return {"User: {user_id} - Deleted": True}

@app.get("/users/{user_id}/organisations", response_model=list[OrganisationPublic])
def get_user_organisations(*, session: Session = Depends(get_session), user_id: int):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    organisations = session.exec(select(Organisation).where(Organisation.owner_id == user_id)).all()

    return organisations