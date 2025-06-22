import os 
from celery import Celery
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

class CeleryConfig:
    @staticmethod
    def create_app() -> Celery:
        app = Celery("metrics_control")

        app.conf.broker_url = os.getenv("CELERY_BROKER_URL")
        app.conf.result_backend = os.getenv("CELERY_RESULT_BACKEND")

        app.conf.task_serializer = "json"
        app.conf.accept_content = ["json"]
        app.conf.broker_connection_retry_on_startup = True
        app.conf.beat_scheduler = "django_celery_beat.schedulers:DatabaseScheduler"
        app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

        return app

