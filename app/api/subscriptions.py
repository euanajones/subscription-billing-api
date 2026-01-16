from fastapi import HTTPException, Query, Depends
from sqlmodel import Session, select
from app.db.models import Subscription, Plan, PlanCreate, PlanPublic, PlanUpdate
from main import app, get_session

@app.get("/subscription")
def get_subscriptions(
    *, 
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=30, le=100)
    ):
    subsriptions = session.exec(select(Subscription)).all()
    return subsriptions