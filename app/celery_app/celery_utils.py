from celery import current_app as current_celery_app, states
from celery.result import AsyncResult

from celery.signals import after_task_publish
import logging
import sys

from app.config import settings


def create_celery():
    celery_app = current_celery_app
    celery_app.config_from_object(settings, namespace="CELERY")

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("[%(asctime)s: %(levelname)s/%(processName)s] %(message)s")
    )
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

    celery_app.logger = logger
    return celery_app


def get_task_info(task_id):
    """
    return task info according to the task_id
    """
    task = AsyncResult(task_id)

    response = {"status": task.state, "id": task_id, "error": None, "result": None}

    if task.state == "FAILURE":
        response.update(
            {
                "error": str(task.info),
            }
        )
    elif task.state == states.SUCCESS:
        response.update({"result": task.get()})

    return response


@after_task_publish.connect
def update_sent_state(sender=None, headers=None, **kwargs):
    # the task may not exist if sent using `send_task` which
    # sends tasks by name, so fall back to the default result backend
    # if that is the case.
    task = current_celery_app.tasks.get(sender)
    backend = current_celery_app.backend

    backend.set(headers["id"], "START")
