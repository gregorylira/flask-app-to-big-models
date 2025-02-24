from flask import Flask
import os
import redis
from rq import Queue

app = Flask(__name__)
app.config["REDIS_URL"] = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_conn = redis.from_url(app.config["REDIS_URL"])

q = Queue(connection=redis_conn)

from app import routes
