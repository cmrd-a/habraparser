import os

from celery import Celery
from celery import signals
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habraparser.settings')

app = Celery('habraparser')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@signals.setup_logging.connect
def on_celery_setup_logging(**kwargs):
    pass


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
