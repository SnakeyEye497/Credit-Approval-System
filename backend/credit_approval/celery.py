import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_approval.settings')

app = Celery('credit_approval')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

