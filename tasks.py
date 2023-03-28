import time
from celery import Celery

app = Celery('crawler', broker='pyamqp://guest@localhost//', backend='redis://localhost')

@app.task
def hello(message: str, secs: int) -> str:
    time.sleep(secs)
    return message
