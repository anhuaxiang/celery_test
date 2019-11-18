from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery.schedules import crontab


broker = 'redis://:redis123321eq@192.168.0.215:6379/6'
backend = 'redis://:redis123321eq@192.168.0.215:6379/6'
app = Celery('periodic', broker=broker, backend=backend)
app.conf.update(result_expires=3600, timezone='Asia/Shanghai')


@app.task
def test(arg):
    print(arg)
    return arg


@app.on_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=14, minute=33),
        test.s('Good Afternoon!'),
    )


if __name__ == '__main__':
    app.worker_main(argv=['-l=debug'])
