# celery_app.py
from celery import Celery
import os

# Get the Redis URL from the environment variable set by Docker Compose.
# It defaults to 'localhost' if the variable isn't set (for local development).
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

celery = Celery(
    'project_titan',
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=['tasks']
)

celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)