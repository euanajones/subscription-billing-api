from fastapi import HTTPException, Query, Depends
from sqlmodel import Session, select
from app.db.models import Plan, PlanCreate, PlanPublic, PlanUpdate
from main import app, get_session

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