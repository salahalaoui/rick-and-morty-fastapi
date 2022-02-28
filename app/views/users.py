from app import crud
from app import models
from app import schema
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.deps import get_current_user
from app.errors import ElementNotFound
from app.database import get_db_session

router = APIRouter()


@router.get(
    "/{user_id}",
    response_model=schema.UserDB,
    summary="get an user by id",
)
def get_user_by_id(user_id: int, db: Session = Depends(get_db_session)):
    user = crud.user.get(db=db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=400,
            detail=f"user {user_id} does not exist",
        )

    return user


@router.patch(
    "/{user_id}",
    response_model=schema.UserDB,
    summary="patch an user by id",
)
def patch_user_by_id(user_id: int, query: schema.UserUpdate, db: Session = Depends(get_db_session), _: models.User = Depends(get_current_user)):
    user = crud.user.get(db, id=user_id)

    if not user:
        raise HTTPException(
            status_code=400,
            detail=f"user {user_id} does not exist",
        )

    return crud.user.update(db=db, db_obj=user, obj_in=query)


@router.delete(
    "/{user_id}",
    response_model=schema.Message,
    summary="delete an user by id",
)
def deleter_user_by_id(user_id: int, db: Session = Depends(get_db_session), _: models.User = Depends(get_current_user)):
    try:
        crud.user.remove(db=db, id=user_id)
    except ElementNotFound as e:
        raise HTTPException(
            status_code=400,
            detail=f"user {user_id} does not exist",
        )

    return schema.Message(message=f"user {user_id} has been deleted from the database")
