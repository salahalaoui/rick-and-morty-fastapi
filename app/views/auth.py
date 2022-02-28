from fastapi import APIRouter

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status

from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

from sqlalchemy.orm import Session

from app.database import db_context, get_db_session
from app.config import settings
from jose import JWTError, jwt
from app import schema
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app import models
from app import crud
from app.models import User

router = APIRouter()


def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def authenticate_user(username: str, password: str):
    with db_context() as session:
        user = crud.user.get_by_username(session, username)

        if not user or not user.check_password(password):
            return False
        return user


@router.post("/token", response_model=schema.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_jwt_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register/", response_model=schema.UserDB)
def register(user: schema.User, db: Session = Depends(get_db_session)):
    existing_user = crud.user.get_by_username(db, user.name)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    return crud.user.create(db=db, obj_in=user)
