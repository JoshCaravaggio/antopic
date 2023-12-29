from __future__ import absolute_import
import os
from celery import Celery
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'antopic.settings')
app = Celery('antopic', )
app.config_from_object('django.conf:settings', namespace='CELERY')

django.setup()