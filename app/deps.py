from fastapi import Depends, HTTPException, status
from fastapi.param_functions import Query
from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar, Union

from fastapi import Depends, HTTPException, status

from app.config import settings
from jose import JWTError, jwt
from app import schema
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app import models
from app.database import db_context
from app import crud
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def common_parameters(
    skip: int = 0,
    limit: int = 20,
    filter: List[str] = Query(
        None,
        description="This filter can accept search query's like `key:value` and will split on the `:`. If it "
                    "detects more than one `:`, or does not find a `:` it will search for the string in all columns.",
    )
) -> Dict[str, Union[List[str], int]]:
    return {"skip": skip, "limit": limit, "filter": filter}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    with db_context() as session:
        user = crud.user.get_by_username(session,  token_data.username)
        if user is None:
            raise credentials_exception
        return user
