import os
import pathlib
from kombu import Queue
from celery.schedules import crontab

from dotenv import load_dotenv

load_dotenv()


def route_task(name, args, kwargs, options, task=None, **kw):
    if ":" in name:
        queue, _ = name.split(":")
        return {"queue": queue}
    return {"queue": "default"}


class BaseConfig:
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent

    DATABASE_URL: str = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR}/db.sqlite3"
    )
    DATABASE_CONNECT_DICT: dict = {}

    SECRET_KEY = os.environ["SECRET_KEY"]
    ALGORITHM = os.environ["ALGORITHM"]
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
    CELERY_BROKER_URL: str = os.environ.get(
        "CELERY_BROKER_URL", "redis://127.0.0.1:6379/0"
    )
    CELERY_RESULT_BACKEND: str = os.environ.get(
        "CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0"
    )

    WS_MESSAGE_QUEUE: str = os.environ.get(
        "WS_MESSAGE_QUEUE", "redis://127.0.0.1:6379/0"
    )
    CELERY_BEAT_SCHEDULE: dict = {
        "periodic_task_example": {
            "task": "periodic_task_example",
            "schedule": crontab(minute="*", hour="*"),
        }
    }

    CELERY_TASK_DEFAULT_QUEUE: str = "default"

    # Force all queues to be explicitly listed in `CELERY_TASK_QUEUES` to help prevent typos
    CELERY_TASK_CREATE_MISSING_QUEUES: bool = False

    CELERY_TASK_QUEUES: list = (
        # need to define default queue here or exception would be raised
        Queue("default"),
        Queue("high_priority"),
        Queue("low_priority"),
    )

    CELERY_TASK_ROUTES = (route_task,)

    UPLOADS_DEFAULT_DEST: str = str(BASE_DIR / "files")
    VERSION = "0.0.1"


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    # https://fastapi.tiangolo.com/advanced/testing-database/
    DATABASE_URL: str = "sqlite:///./test.db"
    DATABASE_CONNECT_DICT: dict = {"check_same_thread": False}


def get_setting():
    config_cls_dict = {
        "dev": DevelopmentConfig,
        "prod": ProductionConfig,
        "test": TestingConfig,
    }

    config_name = os.environ.get("FASTAPI_CONFIG", "dev")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_setting()
