from app.schema.comment import Comment, CommentCreate

from app.database import db_context
from app.models import Character as CharacterModel

from app import schema
from app import models

from app import factories

e = factories.EpisodeFactory.build()

print(e.characters.all())

schema.EpisodeCreate.from_orm(e)

with db_context() as session:
    session.query(models.User).filter(models.User.name == 'string').first()