from app import crud
from app import models
from app import schema
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

from app.deps import get_current_user
from app.errors import ElementNotFound
from app.database import get_db_session
from app import errors

router = APIRouter()


@router.get(
    "/",
    response_model=List[schema.Episode],
    summary="get all episodes",
)
def get_episodes(db: Session = Depends(get_db_session)):
    episodes, _ = crud.episode.get_multi(db)
    return episodes


@router.get(
    "/{episode_id}",
    response_model=schema.EpisodeWithCharacters,
    summary="get episode by id",
)
def get_episode_by_id(episode_id: int, db: Session = Depends(get_db_session)):
    episode = crud.episode.get(db=db, id=episode_id)
    if not episode:
        raise HTTPException(
            status_code=400,
            detail=f"episode {episode_id} does not exist",
        )

    return schema.EpisodeWithCharacters.from_orm(episode)


@router.post(
    "/",
    response_model=schema.Episode,
    summary="post episode",
    status_code=status.HTTP_201_CREATED,
)
def post_episode(query: schema.postEpisodeQuery, db: Session = Depends(get_db_session)):
    try:
        return schema.Episode.from_orm(crud.episode.create(db=db, obj_in=query))
    except errors.CrudError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.patch(
    "/{episode_id}", response_model=schema.Episode, summary="patch episode by id"
)
def patch_episode_by_id(
    episode_id: int,
    query: schema.EpisodeUpdate,
    db: Session = Depends(get_db_session),
    _: models.User = Depends(get_current_user),
):
    episode = crud.episode.get(db, id=episode_id)

    if not episode:
        raise HTTPException(
            status_code=400,
            detail=f"episode {episode_id} does not exist",
        )

    return crud.episode.update(db=db, db_obj=episode, obj_in=query)


@router.delete(
    "/{episode_id}",
    response_model=schema.Message,
    summary="delete episode by id",
)
def delete_episode_by_id(
    episode_id: int,
    db: Session = Depends(get_db_session),
    _: models.User = Depends(get_current_user),
):
    try:
        crud.episode.remove(db=db, id=episode_id)
    except errors.CrudError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    return schema.Message(
        message=f"episode {episode_id} has been deleted from the database"
    )
