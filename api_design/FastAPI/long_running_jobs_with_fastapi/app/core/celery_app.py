# Celery initialization
from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.modules.jobs.tasks"]
)

celery_app.conf.task_track_started = True
celery_app.conf.result_expires = 3600
