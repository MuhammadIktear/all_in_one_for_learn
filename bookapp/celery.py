import os
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookapp.settings')

app = Celery('bookapp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'daily_book_log_email': {
        'task': 'app.tasks.send_daily_book_logs',
        'schedule': crontab(hour=22, minute=0),
        # 'schedule': timedelta(minutes=1),          # for testing every 1 min
    },
}