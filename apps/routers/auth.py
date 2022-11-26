from fastapi import (
    FastAPI,
    HTTPException,
    status,
    Response,
    Depends,
    APIRouter,
)

from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    access_token = oauth.create_access_token(data={"user_id": user.id})
    # print(access_token)
    return {"access_token": access_token, "token_type": "bearer"}

