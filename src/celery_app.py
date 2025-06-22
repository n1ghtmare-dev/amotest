import os
from metrics_control.celery_config import CeleryConfig


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "metrics_control.settings")
celery_app = CeleryConfig.create_app()
