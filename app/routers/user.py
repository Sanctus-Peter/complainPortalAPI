from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, database, models, utils, oauth2

router = APIRouter(tags=["Users"])


@router.post("/register", status_code=status.HTTP_201_CREATED,
             response_model=schemas.User)
async def create_user(user: schemas.CreateUser,
                      db: Session = Depends(database.get_db)):
    user_query = db.query(models.User).filter(user.email == models.User.email).first()

    if user_query:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"User with email {user.email} already exists")

    hashed_password = utils.hashed(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/submitComplaint", status_code=status.HTTP_201_CREATED,
             response_model=schemas.Complain)
async def user_complain(
        usr_complain: schemas.PostComplain,
        db: Session = Depends(database.get_db),
        user: int = Depends(oauth2.get_current_user)
):
    new_complain = models.Complain(owner_id=user.id, **usr_complain.dict())
    db.add(new_complain)
    db.commit()
    db.refresh(new_complain)
    return new_complain


@router.get("/getAllComplaintsForUser", response_model=list[schemas.UserComplain])
def get_all_complains(db: Session = Depends(database.get_db),
                      user: int = Depends(oauth2.get_current_user)):
    complains = db.query(models.Complain).filter(
        models.Complain.owner_id == user.id).all()
    return complains


@router.get("/viewComplaints", response_model=list[schemas.Complain])
def view_complain_details(db: Session = Depends(database.get_db),
                          user: int = Depends(oauth2.get_current_user)):
    complains = db.query(models.Complain).filter(
        models.Complain.owner_id == user.id).all()
    return complains
