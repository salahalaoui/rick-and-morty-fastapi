from typing import Optional, List

from pydantic import BaseModel, validator, root_validator
from datetime import datetime


class CommentCreateQuery(BaseModel):
    character_id: Optional[int]
    episode_id: Optional[int]
    body: str

    class Config:
        orm_mode = True

    @root_validator
    def any_of(cls, v):
        if not v["character_id"] and not v["episode_id"]:
            raise ValueError("one of character_id, episode_id must have a value")
        return v


class CommentCreate(CommentCreateQuery):
    user_id: int


class Comment(CommentCreate):
    id: int
    created_at: datetime
    updated_at: datetime


class Comments(BaseModel):
    comments: List[Comment]


class CommentUpdate(BaseModel):
    body: str
