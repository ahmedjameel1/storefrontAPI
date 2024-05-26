import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings.dev')

celery = Celery('storefront')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.conf.update(timezone='Africa/Cairo')

celery.conf.beat_schedule = {
    'notify_customers': {
        'task': 'playground.tasks.notify_customers',
        'schedule': crontab(day_of_week='3', hour=22, minute=31),
        'args': ['Hello wednesday']
    }
}

celery.autodiscover_tasks()

