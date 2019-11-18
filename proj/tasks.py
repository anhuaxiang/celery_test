from __future__ import absolute_import, unicode_literals
from celery.utils.log import get_task_logger
from celery.exceptions import Ignore, Reject
from celery.schedules import crontab
from .celery import app
import time

logger = get_task_logger(__name__)


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(mumbers):
    return sum(mumbers)


@app.task
def test(arg):
    print(arg)
    return arg


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=14, minute=42),
        test.s('Good Afternoon!'),
    )


@app.task(bind=True)
def my_retry_test_1(self):
    try:
        1 / 0
    except Exception as e:
        time.sleep(5)
        raise self.retry(exc=e)


@app.task(bind=True, default_retry_delay=5)  # retry in 5s.
def my_retry_test_2(self, x, y):
    try:
        return x / y
    except Exception as exc:
        # overrides the default delay to retry after 10 s
        raise self.retry(exc=exc, countdown=10)


@app.task(autoretry_for=(ValueError,), retry_kwargs={'max_retries': 5})
def my_retry_test_3():
    raise ValueError()


@app.task(autoretry_for=(ValueError,), retry_backoff=True)
def my_retry_test_4():
    raise ValueError()


@app.task(bind=True)
def my_status_task(self, filenames):
    for i, f in enumerate(filenames):
        logger.debug(f'process {i} th, data: {f}')
        self.update_state(state='PROGRESS', meta={'current': i, 'total': len(filenames)})
        time.sleep(2)
    return 'ok'


@app.task(bind=True)
def ignore_task(self, user):
    logger.info(f'task.request: {self.request.id}')
    raise Ignore()


@app.task(bind=True)
def reject_test(self):
    raise Reject('no reason', requeue=False)


@app.task(bind=True, acks_late=True)
def reject_test_redo(self):
    raise Reject('no reason', requeue=True)


@app.task(ignore_result=True)
def ignore_result_task():
    return 'ok'


@app.task(bind=True)
def hello(self, a, b):
    time.sleep(1)
    self.update_state(state='PROGRESS', meta={'progress': 50})
    time.sleep(5)
    self.update_state(state='PROGRESS', meta={'progress': 90})
    time.sleep(5)
    return f'hello world: {a + b}'
