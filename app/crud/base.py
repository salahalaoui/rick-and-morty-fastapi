from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, Tuple

from app.database import Base, db_context
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect as sa_inspect
from sqlalchemy import String, cast, or_
from more_itertools import one
from datetime import datetime

from app.errors import ElementNotFound

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 500,
        filter_parameters: Optional[List[str]] = None
    ) -> Tuple[List[ModelType], str]:
        conditions = []
        query = db.query(self.model)

        print(f'filter_parameters {filter_parameters}')
        if filter_parameters:
            for filter_parameter in filter_parameters:
                key, *value = filter_parameter.split(":", 1)
                print(value)
                # Use this branch if we detect a key value search (key:value) if it is just a single string (value)
                # treat the key as the value
                if len(value) > 0:
                    if key in sa_inspect(self.model).columns.keys():
                        conditions.append(cast(self.model.__dict__[key], String).ilike("%" + one(value) + "%"))
                    query = query.filter(or_(*conditions))
                else:
                    for column in sa_inspect(self.model).columns.keys():
                        conditions.append(cast(self.model.__dict__[column], String).ilike("%" + key + "%"))
                    query = query.filter(or_(*conditions))
        count = query.count()
        print(query)
        if limit:
            # Limit is not 0: use limit
            response_range = "{} {}-{}/{}".format(self.model.__table__.name.lower(), skip, skip + limit, count)
            return query.offset(skip).limit(limit).all(), response_range
        else:
            # Limit is 0: unlimited
            response_range = "{} {}/{}".format(self.model.__table__.name.lower(), skip, count)
            return query.offset(skip).all(), response_range

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        if 'updated_at' in self.model.__dict__:
            db_obj.updated_at = datetime.utcnow()

        db.add(db_obj)
        db.commit()
        return db_obj

    def remove(self, db: Session, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        if not obj:
            raise ElementNotFound(f"entity {id} does not exist")
        db.delete(obj)
        db.commit()
        return obj
