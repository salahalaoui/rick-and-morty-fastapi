from app import crud
from app.database import db_context
from typing import List
from starlette.responses import Response
from sqlalchemy.orm import Session

from app import schema
from fastapi import APIRouter, HTTPException, Depends, status
from app.errors import ElementNotFound
from app.deps import common_parameters
from app.database import get_db_session
from app.deps import get_current_user
from app import models

router = APIRouter()


@router.get(
    "/",
    response_model=List[schema.Character],
    summary="get all characters",
)
def get_characters(
    response: Response,
    common: dict = Depends(common_parameters),
    db: Session = Depends(get_db_session),
):
    characters, header_range = crud.character.get_multi(
        db=db,
        skip=common["skip"],
        limit=common["limit"],
        filter_parameters=common["filter"],
    )
    response.headers["Content-Range"] = header_range
    return characters


@router.get(
    "/{character_id}",
    response_model=schema.Character,
    summary="get character by id",
)
def get_character_by_id(character_id: int, db: Session = Depends(get_db_session)):
    character = crud.character.get(db, character_id)
    if not character:
        raise HTTPException(
            status_code=400,
            detail=f"character {character_id} does not exist",
        )

    return character


@router.post(
    "/",
    response_model=schema.Character,
    summary="post character",
    status_code=status.HTTP_201_CREATED,
)
def post_character(
    query: schema.CharacterCreate, db: Session = Depends(get_db_session)
):
    return crud.character.create(db, query)


@router.patch(
    "/{character_id}",
    response_model=schema.Character,
    summary="patch character by id",
)
def patch_character_by_id(
    character_id: int,
    query: schema.CharacterUpdate,
    db: Session = Depends(get_db_session),
    _: models.User = Depends(get_current_user),
):
    character = crud.character.get(db=db, id=character_id)

    if not character:
        raise HTTPException(
            status_code=400,
            detail=f"character {character_id} does not exist",
        )

    return crud.character.update(db=db, db_obj=character, obj_in=query)


@router.delete(
    "/{character_id}",
    summary="delete character by id",
)
def delete_character_by_id(
    character_id: int,
    db: Session = Depends(get_db_session),
    _: models.User = Depends(get_current_user),
):
    try:
        crud.character.remove(db=db, id=character_id)
    except ElementNotFound:
        raise HTTPException(
            status_code=400,
            detail=f"character {character_id} does not exist",
        )

    return schema.Message(
        message=f"character {character_id} has been deleted from the database"
    )
