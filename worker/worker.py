import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rq import Queue, SimpleWorker

from core.queue import redis_conn

listen = ["tasks"]

if __name__ == "__main__":
    queues = [Queue(name, connection=redis_conn) for name in listen]
    worker = SimpleWorker(queues, connection=redis_conn)
    worker.work()
