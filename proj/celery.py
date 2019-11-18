from __future__ import absolute_import, unicode_literals
from celery import Celery


# broker = 'redis://:redis123321eq@192.168.0.215:6379/4'
# backend = 'redis://:redis123321eq@192.168.0.215:6379/4'
# include = ['proj.tasks']
# app = Celery('proj', broker=broker, backend=backend, include=include, )


# app.conf.update(result_expires=3600, timezone='Asia/Shanghai')
# app.conf.update(
#     task_serializer='json',
#     accept_content='json',
#     result_serializer='json',
#     timezone='Asia/Shanghai',
#     enable_utc=False
# )

app = Celery('proj')
app.config_from_object('proj.celery_config')


if __name__ == '__main__':
    app.start()
