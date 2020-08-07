import os

from celery import Celery
from celery import signals
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "habraparser.settings")

app = Celery("habraparser")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@signals.setup_logging.connect
def on_celery_setup_logging(**kwargs):
    """Отключение встроенного логирования"""
    pass


app.conf.timezone = "Europe/Moscow"

app.conf.beat_schedule = {
    "parse_daily": {
        "task": "core.tasks.parse_daily",
        "schedule": crontab(minute=0, hour=15),
    }
}
