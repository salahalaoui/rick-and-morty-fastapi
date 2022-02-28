from app.crud.base import CRUDBase
from app import schema
from app import models


class CRUDComment(CRUDBase[models.Comment, schema.CommentCreate, schema.CommentUpdate]):
    ...


comment = CRUDComment(models.Comment)
