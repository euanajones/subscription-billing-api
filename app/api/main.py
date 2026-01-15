from fastapi import FastAPI, HTTPException, Query, Depends
from sqlmodel import SQLModel, Session, create_engine, select
from app.settings.config import settings
from app.db.models import Plan, PlanPublic, PlanCreate, PlanUpdate
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