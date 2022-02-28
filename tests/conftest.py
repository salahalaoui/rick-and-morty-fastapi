import os
from typing import Generator

import pytest
from sqlalchemy.orm import sessionmaker

from app.database import SessionLocal
from contextlib import contextmanager

os.environ["FASTAPI_CONFIG"] = "test"

from pytest_factoryboy import register
from app.factories import UserFactory, EpisodeFactory
from app import models

register(UserFactory)
register(EpisodeFactory)


@pytest.fixture
def settings():
    from app.config import settings as _settings

    return _settings


@pytest.fixture
def app(settings):
    from app import create_app

    app = create_app()
    return app


@pytest.fixture()
def db_session(app):
    from app.database import Base, engine, SessionLocal

    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(app):
    from fastapi.testclient import TestClient

    yield TestClient(app)


@pytest.fixture(autouse=True)
def tmp_upload_dir(tmpdir, settings):
    settings.UPLOADS_DEFAULT_DEST = tmpdir.mkdir("tmp")
