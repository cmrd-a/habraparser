from celery.schedules import crontab
from celery.utils.log import get_task_logger
import os
from celery import Celery
from celery import signals
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habraparser.settings')

app = Celery('habraparser')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@signals.setup_logging.connect
def on_celery_setup_logging(**kwargs):
    pass


# app.conf.beat_schedule = {
#     'every-minute': {
#         'task': 'core.tasks.parse_pages_list',
#         'schedule': crontab(),
#     },
# }
