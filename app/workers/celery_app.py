from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "sentinel",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.workers.incident_tasks"]
)

celery_app.autodiscover_tasks(["app.workers"])