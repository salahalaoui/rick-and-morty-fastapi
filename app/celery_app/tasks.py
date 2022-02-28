from celery import shared_task

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(name="periodic_task_example")
def create_task():
    """just an example of a celery periodic task"""
    logger.info("periodic_task_example")
