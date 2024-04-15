import logging
import os

from celery import Celery, signals

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kaos.settings")

app = Celery(
    "backend",
)
# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.beat_scheduler = "django_celery_beat.schedulers.DatabaseScheduler"
app.conf.worker_cancel_long_running_tasks_on_connection_loss = True


@signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    return logging.getLogger("celery")
