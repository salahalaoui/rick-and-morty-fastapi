from pydantic import BaseModel, root_validator
from typing import List, Optional, Set
from datetime import datetime


class User(BaseModel):
    name: str
    password: str


class UserUpdate(BaseModel):
    name: str


class UserDB(BaseModel):
    id: int
    name: str
    password: str
    created_at: datetime

    class Config:
        orm_mode = True
