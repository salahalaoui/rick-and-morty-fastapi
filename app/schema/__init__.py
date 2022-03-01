from typing import Any, Optional

from pydantic import BaseModel, validator
from sqlalchemy.orm import Query


class Message(BaseModel):
    message: str


class OrmBase(BaseModel):
    # Common properties across orm models
    id: int

    # Pre-processing validator that evaluates lazy relationships before any other validation
    # NOTE: If high throughput/performance is a concern, you can/should probably apply
    #       this validator in a more targeted fashion instead of a wildcard in a base class.
    #       This approach is by no means slow, but adds a minor amount of overhead for every field
    @validator("*", pre=True)
    def evaluate_lazy_columns(cls, v):
        if isinstance(v, Query):
            return v.all()
        return v

    class Config:
        orm_mode = True


from app.schema.character import (
    Character,
    Characters,
    CharacterUpdate,
    CharacterCreate,
    CharacterCreateJson,
)
from app.schema.auth import Task, TaskResult, Token, TokenData
from app.schema.comment import (
    Comment,
    CommentUpdate,
    Comments,
    CommentCreate,
    CommentCreateQuery,
)
from app.schema.episode import (
    Episode,
    EpisodeCreate,
    EpisodeDB,
    Episodes,
    EpisodeUpdate,
    EpisodeWithCharacters,
    EpisodeCreateJson,
    postEpisodeQuery,
)
from app.schema.user import User, UserUpdate, UserDB
