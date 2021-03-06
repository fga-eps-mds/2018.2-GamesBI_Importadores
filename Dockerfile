FROM python:3.6-jessie

RUN apt-get update && apt-get install git

ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0
ENV C_FORCE_ROOT true

COPY . /queue
WORKDIR /queue/worker

RUN pip install -r requirements.txt

CMD celery -A tasks worker -B -l debug
