import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('Newsportal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send_weekly_notification': {
        'task': 'news.tasks.weekly_notification',
        'schedule': crontab(day_of_week='tuesday')
    },
}

app.autodiscover_tasks()