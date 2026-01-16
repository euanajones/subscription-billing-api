from fastapi import HTTPException, Query, Depends
from sqlmodel import Session, select
from app.db.models import Subscription, SubscriptionPublic  
from main import app, get_session

@app.get("/subscription", response_model=SubscriptionPublic)
def get_subscriptions(
    *, 
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=30, le=100)
    ):
    subsriptions = session.exec(select(Subscription)).all()
    return subsriptions

@app.get("/subscription\{sub_id}", response_model=SubscriptionPublic)
def get_subscription_by_id(*, session: Session = Depends(get_session), sub_id: int):
    subscription = session.exec(Subscription, sub_id)

    if not subscription:
        HTTPException(status_code=404, detail="Subscription not found.")
    return subscription