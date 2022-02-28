from app.crud.base import CRUDBase
from app import schema
from app import models


class CRUDCharacter(CRUDBase[models.Character, schema.CharacterCreate, schema.CharacterUpdate]):
    ...


character = CRUDCharacter(models.Character)
