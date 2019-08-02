
import os

from celery import Celery

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'

#创建应用
celery_app=Celery('meiduo')

#导入配置
celery_app.config_from_object('celery_tasks.config')

#自动注册celery应用
celery_app.autodiscover_tasks(['celery_tasks.sms','celery_tasks.email','celery_tasks.html'])