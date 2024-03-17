import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'group_donations.settings')

app = Celery('group_donations')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
