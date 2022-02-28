from app import crud
from app import schema
from sqlalchemy.orm import Session
from datetime import datetime
from tests.utils.utils import random_date, random_lower_string
import random


def test_created_episode(db_session: Session) -> None:

    fake_member = schema.postEpisodeQuery(
        name=random_lower_string(),
        episode=random.randint(1, 30),
        season=random.randint(1, 30),
        air_date=random_date()
    )
    episode = crud.episode.create(db_session, fake_member)

    assert episode.name == fake_member.name
    assert episode.episode == fake_member.episode
    assert episode.season == fake_member.season
    assert episode.air_date == fake_member.air_date


def test_get_episode(db_session: Session) -> None:

    fake_member = schema.postEpisodeQuery(
        name=random_lower_string(),
        episode=random.randint(1, 30),
        season=random.randint(1, 30),
        air_date=random_date()
    )
    episode = crud.episode.create(db_session, fake_member)

    episode_db = crud.episode.get(db_session, episode.id)
    assert episode.name == episode_db.name
    assert episode.episode == episode_db.episode
    assert episode.season == episode_db.season
    assert episode.air_date == episode_db.air_date


def test_patch_episode(db_session: Session) -> None:

    fake_member = schema.postEpisodeQuery(
        name=random_lower_string(),
        episode=random.randint(1, 30),
        season=random.randint(1, 30),
        air_date=random_date()
    )
    episode = crud.episode.create(db_session, fake_member)
    updated_fake_member = schema.EpisodeUpdate(
        name=random_lower_string(),
        air_date=random_date()
    )
    episode_db = crud.episode.update(db=db_session, db_obj=episode, obj_in=updated_fake_member)
    episode_db = crud.episode.get(db=db_session, id=episode_db.id)
    assert episode_db.name == updated_fake_member.name
    assert episode_db.air_date == updated_fake_member.air_date


def test_delete_episode(db_session: Session) -> None:

    fake_member = schema.postEpisodeQuery(
        name=random_lower_string(),
        episode=random.randint(1, 30),
        season=random.randint(1, 30),
        air_date=random_date()
    )
    episode = crud.episode.create(db_session, fake_member)

    crud.episode.remove(db_session, episode.id)
    db_episode = crud.episode.get(db_session, episode.id)

    assert not db_episode


