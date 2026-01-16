from fastapi import HTTPException, Query, Depends
from sqlmodel import Session, select
from app.db.models import User, UserPublic, Organisation, OrganisationPublic, OrganisationUpdate, OrganisationPublicWithOwner, OrganisationCreate
from main import app, get_session

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

@app.get("/organisations", response_model=OrganisationPublic)
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