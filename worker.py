from redis import Redis
from rq import Worker, Queue
from dotenv import load_dotenv

load_dotenv()

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
conn = Redis.from_url(redis_url)

queue = Queue("default", connection=conn)

worker = Worker([queue], connection=conn)

if __name__ == "__main__":
    worker.work()
