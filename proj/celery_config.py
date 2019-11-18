from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
from datetime import timedelta

broker_url = 'redis://:redis123321eq@192.168.0.215:6379/6'
result_backend = 'redis://:redis123321eq@192.168.0.215:6379/7'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Shanghai'
enable_utc = False
result_expires = 60 * 60

imports = [
    'proj.tasks',
]

# task_routes = {
#     'tasks.add': 'low-priority'
# }
#
# task_annotations = {
#     'tasks.add': {'rate_limit': '10/m'}
# }


beat_schedule = {
    'test1': {
        'task': 'proj.tasks.test',
        'schedule': timedelta(seconds=10),
        'args': ('hello',)
    }
}