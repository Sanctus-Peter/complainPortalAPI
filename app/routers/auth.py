from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, database, models, utils, oauth2

router = APIRouter(tags=["Authentication"],)


@router.post("/login", response_model=schemas.UserLogin)
def user_login(usr_credentials: OAuth2PasswordRequestForm = Depends(),
               db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == usr_credentials.username).first()
    if not user or not utils.verify(usr_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid login credentials")
    access_tok = oauth2.create_access_token(data={"user_id": user.id})
    return {
        "name": user.name,
        "access_token": access_tok,
        "token_type": "bearer",
        "id": user.id
    }