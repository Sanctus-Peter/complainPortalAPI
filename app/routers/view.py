from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import database, models, oauth2, schemas

router = APIRouter(tags=["View all complains"])


@router.get("/viewComplaints", response_model=list[schemas.Complain])
async def view_all_complains_details(db: Session = Depends(database.get_db),
                               user: int = Depends(oauth2.get_current_user)):
    is_admin = user.role == "admin"
    if is_admin:
        complains = db.query(models.Complain).all()
    else:
        complains = db.query(models.Complain).filter(
            models.Complain.owner_id == user.id).all()
    return complains
