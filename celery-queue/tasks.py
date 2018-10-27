import os
import time
import requests
from celery import Celery
from celery.schedules import crontab



CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

CELERY_BEAT_SCHEDULE = {
    'import': {
        'task': 'tasks.import',
        'schedule': crontab('0', '1', '*', '*', '*')
    }
}

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
celery.conf.beat_schedule = CELERY_BEAT_SCHEDULE

@celery.task(name='tasks.import')
def import():
    print("Starting request")
    req = requests.get(os.environ['IMPORTER_GET'])
    requests.post(os.environ['CROSSDATA_POST'], json=req.json())
