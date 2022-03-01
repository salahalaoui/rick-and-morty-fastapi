import os
from typing import List
from uuid import uuid4 as uuid

import pandas
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import FileResponse, Response

from app import crud, models, schema
from app.config import settings
from app.database import get_db_session
from app.deps import common_parameters, get_current_user
from app.errors import ElementNotFound

router = APIRouter()


@router.get(
    "/",
    response_model=List[schema.Comment],
    summary="get all comments",
)
def get_comments(
    response: Response,
    common: dict = Depends(common_parameters),
    db: Session = Depends(get_db_session),
):
    comments, header_range = crud.comment.get_multi(
        db=db,
        skip=common["skip"],
        limit=common["limit"],
        filter_parameters=common["filter"],
    )
    response.headers["Content-Range"] = header_range
    return comments


@router.post(
    "/",
    response_model=schema.Comment,
    summary="post a comment",
    status_code=status.HTTP_201_CREATED,
)
def post_comment(
    query: schema.CommentCreateQuery,
    db: Session = Depends(get_db_session),
    current_user: models.User = Depends(get_current_user),
):
    if query.episode_id:
        episode = crud.episode.get(db=db, id=query.episode_id)
        if not episode:
            raise HTTPException(
                status_code=400,
                detail=f"episode {query.episode_id} does not exist",
            )
    if query.character_id:
        character = crud.character.get(db=db, id=query.character_id)
        if not character:
            raise HTTPException(
                status_code=400,
                detail=f"character {query.episode_id} does not exist",
            )
    return crud.comment.create(
        db=db, obj_in=schema.CommentCreate(**dict(query), user_id=current_user.id)
    )


@router.patch(
    "/{comment_id}",
    response_model=schema.Comment,
    summary="patch a comment by id",
)
def patch_comment_by_id(
    comment_id: int,
    query: schema.CommentUpdate,
    db: Session = Depends(get_db_session),
    _: models.User = Depends(get_current_user),
):
    comment = crud.comment.get(db=db, id=comment_id)

    if not comment:
        raise HTTPException(
            status_code=400,
            detail=f"comment {comment_id} does not exist",
        )

    return schema.Comment.from_orm(
        crud.comment.update(db=db, db_obj=comment, obj_in=query)
    )


@router.delete(
    "/{comment_id}",
    response_model=schema.Message,
    summary="delete a comment by id",
)
def delete_comment_by_id(
    comment_id: int,
    db: Session = Depends(get_db_session),
    _: models.User = Depends(get_current_user),
):
    try:
        crud.comment.remove(db=db, id=comment_id)
    except ElementNotFound as e:
        raise HTTPException(
            status_code=400,
            detail=f"comment {comment_id} does not exist",
        )

    return schema.Message(
        message=f"comment {comment_id} has been deleted from the database"
    )


@router.get(
    "/extract",
    summary="download an extract",
)
def download_extract(
    response: Response,
    common: dict = Depends(common_parameters),
    db: Session = Depends(get_db_session),
):
    comments, _ = crud.comment.get_multi(
        db=db,
        skip=common["skip"],
        limit=common["limit"],
        filter_parameters=common["filter"],
    )

    output_filename = f"{uuid()}.csv"
    file_location_full_path = os.path.join(
        settings.UPLOADS_DEFAULT_DEST, output_filename
    )

    content = pandas.DataFrame(
        [dict(schema.Comment.from_orm(comment)) for comment in comments]
    ).to_csv(index=False, sep=";")
    with open(file_location_full_path, "w+") as file_object:
        file_object.write(content)

    return FileResponse(
        file_location_full_path,
        media_type="application/octet-stream",
        filename=output_filename,
    )
