
from celery.schedules import crontab

from . import app

app.conf.beat_schedule = {
    'crawl_stock_yesterday_history_data': {
        'task': 'tasks.crawl_all_stock_history_data',
        'schedule': crontab(hour=1, minute=0),
        'kwargs': dict(weeks=0, days=1)
    }
}
