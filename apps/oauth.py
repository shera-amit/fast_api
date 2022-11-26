from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#SECRET_KEY
#ALGORITHM
#EXPIRATION_TIME


# use "openssl rand -hex 32" to generate a secret key

SECRET_KEY = "f32c967e27bd4aaac8497f886cd9f15c90f49c6bfa6241fb92936c7f6e7482e9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data
    
# def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     token_data = oauth.verify_access_token(token, credentials_exception)
#     user = db.query(models.User).filter(models.User.id == token_data.id).first()
#     if user is None:
#         raise credentials_exception
#     return user


# 7:23:17 Hrs.