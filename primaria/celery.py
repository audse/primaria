import os
from celery import Celery
from celery.schedules import timedelta

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "primaria.settings")

app = Celery("primaria")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "decrease-pet-stats": {
        "task": "core.tasks.decrease_pet_stats",
        "schedule": timedelta(hours=1).total_seconds(),
        "args": (),
    },
    "restock": {
        "task": "shop.tasks.restock",
        "schedule": timedelta(minutes=10).total_seconds(),
        "args": (),
    },
}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
