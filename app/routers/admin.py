from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import database, models, oauth2, schemas

router = APIRouter(tags=["Admins"])


@router.post("/resolveComplaint", status_code=status.HTTP_201_CREATED,
             response_model=schemas.Complain)
def resolve_complain(
        complain: schemas.Resolved,
        db: Session = Depends(database.get_db),
        user: int = Depends(oauth2.get_current_user)
):
    found_complain = db.query(models.Complain).filter(
        complain.id == models.Complain.id)
    is_complain = found_complain.first()
    is_admin = user.role == "admin"
    if not is_complain:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No complain with that id found")
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Unauthorized to perform this request")

    found_complain.update({"resolved": "resolved"}, synchronize_session=False)
    db.commit()
    return found_complain.first()


@router.get("/getAllComplaintsForAdmin", response_model=list[schemas.AllComplain])
def get_all_complains(db: Session = Depends(database.get_db),
                      user: int = Depends(oauth2.get_current_user)):
    is_admin = user.role == "admin"
    print(is_admin)
    if not is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Unauthorized to perform this request")
    complains = db.query(models.Complain).all()
    return complains
