from unittest import mock

import requests

from app import models


def test_post_login_for_access_token(
    client, db_session, settings, monkeypatch, user_factory
):
    mock_requests_post = mock.MagicMock()
    monkeypatch.setattr(requests, "post", mock_requests_post)

    monkeypatch.setattr(settings, "CELERY_TASK_ALWAYS_EAGER", True, raising=False)

    fake_member = user_factory.build()

    user = models.User(name=fake_member.name)
    user.set_password(fake_member.password)

    db_session.add(user)
    db_session.commit()
    assert user.id

    response = client.post(
        "/token", data={"username": fake_member.name, "password": fake_member.password}
    )
    assert response.status_code == 200

    response_data = response.json()

    assert response_data["token_type"] == "bearer"


def test_register(client, db_session, settings, monkeypatch, user_factory):
    mock_requests_post = mock.MagicMock()
    monkeypatch.setattr(requests, "post", mock_requests_post)

    monkeypatch.setattr(settings, "CELERY_TASK_ALWAYS_EAGER", True, raising=False)

    fake_member = user_factory.build()

    user = models.User(name=fake_member.name)
    user.set_password(fake_member.password)

    db_session.add(user)
    db_session.commit()
    assert user.id
