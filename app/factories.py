import factory
from factory.fuzzy import FuzzyText, FuzzyInteger, FuzzyDateTime
from datetime import datetime, timezone
from app.database import SessionLocal
from app import models


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.User
        sqlalchemy_session = SessionLocal()
        sqlalchemy_get_or_create = ("name",)
        sqlalchemy_session_persistence = "commit"

    name = FuzzyText(length=6)
    password = FuzzyText(length=256)


class EpisodeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.Episode
        sqlalchemy_session = SessionLocal()
        sqlalchemy_get_or_create = ("name", "air_date", "episode", "season")
        sqlalchemy_session_persistence = "commit"

    name = FuzzyText(length=6)
    episode = FuzzyInteger(low=1, high=20)
    season = FuzzyInteger(low=1, high=20)
    air_date = FuzzyDateTime(datetime(2008, 1, 1, tzinfo=timezone.utc))
