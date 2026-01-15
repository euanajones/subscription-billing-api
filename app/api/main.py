from fastapi import FastAPI, HTTPException, Query, Depends
from sqlmodel import SQLModel, Session, create_engine, select
from app.settings.config import settings
from app.db.models import User, UserCreate, UserPublic, UserUpdate, Organisation, OrganisationCreate, OrganisationPublic, OrganisationPublicWithOwner, OrganisationUpdate, Plan, PlanPublic, PlanCreate, PlanUpdate
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

@app.post("/organisations/create", response_model=OrganisationPublic)
def create_organisation(
    *, 
    session: Session = Depends(get_session), 
    organisation: OrganisationCreate
    ):
    db_organisation = Organisation.model_validate(organisation)
    session.add(db_organisation)
    session.commit()
    session.refresh(db_organisation)
    return db_organisation

@app.get("/organisations", response_model=list[OrganisationPublic])
def get_organisations(
    *, 
    session: Session = Depends(get_session), 
    offset: int = 0, 
    limit: int = Query(default=30, le=100)
    ):
    organisations = session.exec(select(Organisation)).all()
    return organisations

@app.get("/organisations/{org_id}", response_model=OrganisationPublicWithOwner)
def get_organisation_by_id(*, session: Session = Depends(get_session), org_id: int):
    organisation = session.get(Organisation, org_id)

    if not organisation:
        raise HTTPException(status_code=404, detail=f"Organisation not found.")
    return organisation

@app.get("/organisations/{org_id}/owner", response_model=UserPublic)
def get_organisation_owner(*, session: Session = Depends(get_session), org_id: int):
    organisation = session.get(Organisation, org_id)

    if not organisation:
        raise HTTPException(status_code=404, detail=f"Organisation not found.")
    owner_id = organisation.owner_id

    if not owner_id:
        raise HTTPException(status_code=404, detail="Organisation owner not set.")

    owner = session.get(User, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found.")

    return owner

@app.delete("/organisation/{org_id}")
def delete_organisation_by_id(*, session: Session = Depends(get_session), org_id: int):
    organisation = session.get(Organisation, org_id)

    if not organisation:
        raise HTTPException(status_code=404, detail="Organisation not found.")
    
    session.delete(organisation)
    session.commit()

    return {"Organisation: {org_id} - Deleted": True}

@app.patch("/organisation/{org_id}", response_model=OrganisationPublic)
def update_organisation(*, session: Session = Depends(get_session), org_id: int, organisation: OrganisationUpdate):
    db_organisation = session.get(Organisation, org_id)

    if not db_organisation:
        raise HTTPException(status_code=404, detail="Organisation not found.")
    
    organisation_data = organisation.model_dump(exclude_unset=True)

    db_organisation.sqlmodel_update(organisation_data)
    session.add(db_organisation)
    session.commit()
    session.refresh(db_organisation)

    return db_organisation

@app.get("/plan", response_model=PlanPublic)
def get_plans(
    *, 
    session: Session = Depends(get_session), 
    offset: int = 0, 
    limit: int = Query(default=30, le=100)
    ):
    plans = session.exec(select(Plan)).all()
    return plans

@app.get("/plans/{plan_id}", response_model=PlanPublic)
def get_plan_by_id(*, session: Session = Depends(get_session) ,plan_id: int):
    plan = session.get(Plan, plan_id)
    
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found.")
    return plan

@app.post("/plans/create", response_model=PlanPublic)
def create_plan(*, session: Session = Depends(get_session), plan: PlanCreate):
    db_plan = Plan.model_validate(plan)
    session.add(db_plan)
    session.commit()
    session.refresh(db_plan)

    return db_plan

@app.patch("/plan/{plan_id}", response_model=PlanPublic)
def update_plan(*, session: Session = Depends(get_session), plan_id: int, plan: PlanUpdate):
    db_plan = session.exec(Plan, plan_id)

    if not db_plan:
        HTTPException(status_code=404, detail="Plan not found.")

    plan_data = plan.model_dump(exclude_unset=True)

    db_plan.sqlmodel_update(plan_data)
    session.add(db_plan)
    session.commit()
    session.refresh(db_plan)

    return db_plan

@app.delete("/plan/{plan_id}")
def delete_plan(*, session: Session = Depends(get_session), plan_id: int):
    plan = session.exec(Plan, plan_id)

    if not plan:
        HTTPException(status_code=404, detail="Plan not found.")

    session.delete(plan)
    session.commit()
    
    return {"Plan: {plan_id} - Deleted": True}