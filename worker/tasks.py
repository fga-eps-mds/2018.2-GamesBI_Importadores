import os
import time
import requests
from celery import Celery
from celery.schedules import crontab
from resources.Importer import Importer


CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

CELERY_BEAT_SCHEDULE = {
    'import_data': {
        'task': 'tasks.import',
        'schedule': crontab(os.environ.get('CELERY_MIN'), os.environ.get('CELERY_HOUR'), '*', '*', '*')
    }
}

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
celery.conf.beat_schedule = CELERY_BEAT_SCHEDULE

@celery.task(name='tasks.import')
def import_data():
    print("Starting request")
    importer = Importer()
    req = importer.get()
    requests.post(os.environ['CROSSDATA_POST'], json=req)
