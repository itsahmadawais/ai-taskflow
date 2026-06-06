import redis
from rq import Queue

from core.config import settings

redis_conn = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

task_queue = Queue("tasks", connection=redis_conn)
