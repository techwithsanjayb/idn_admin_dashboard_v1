from __future__ import absolute_import, unicode_literals
import os
from celery.schedules import crontab
from celery import Celery
import logging.config
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','idn_admin_dashboard.settings')
app = Celery('idn_admin_dashboard')
app.conf.enable_utc = False
app.conf.update(timezone= 'Asia/Kolkata')


# app.config_from_object('django.conf:settings',namespace='CELERY')
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

    
# Configure logging to send logs to stdout
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Apply logging configuration
logging.config.dictConfig(LOGGING)