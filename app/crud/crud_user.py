from app.crud.base import CRUDBase, CreateSchemaType, ModelType
from app import schema
from app import models
from sqlalchemy.orm import Session

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, Tuple


class CRUDUser(CRUDBase[models.User, schema.User, schema.UserUpdate]):
    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(name=obj_in.name)  # type: ignore
        db_obj.set_password(obj_in.password)
        db.add(db_obj)
        db.commit()
        return db_obj

    def get_by_username(self, db: Session, username: str) -> Optional[models.User]:
        return db.query(self.model).filter(self.model.name == username).first()


user = CRUDUser(models.User)
