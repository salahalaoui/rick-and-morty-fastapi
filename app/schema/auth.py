from pydantic import BaseModel
from typing import Optional, Any


class User(BaseModel):
    name: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class TaskResult(BaseModel):
    id: str
    status: str
    error: Optional[str] = None
    result: Optional[Any] = None


class Task(BaseModel):
    task_id: str


class downnloadFromBucketSchema(BaseModel):
    year: str = "2021"
    month: str = "04"
    filename: str = "events.csv"
