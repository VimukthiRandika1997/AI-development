# Background worker (Celery/RQ/etc.)
# Lightweight worker that listens to 'webhooks' queue and processes jobs by importing the function.
# Using RQ's worker class gives more features, but for a small example we'll use a simple loop.

from rq import Worker, Queue, Connection
from redis import Redis
from app.core.config import settings

listen = ["webhooks"]
redis_conn = Redis.from_url(settings.REDIS_URL)

if __name__ == "__main__":
    with Connection(redis_conn):
        worker = Worker(map(Queue, listen))
        worker.work(with_scheduler=True)