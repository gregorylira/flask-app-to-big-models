from flask import Flask
import os
import redis
from rq import Queue
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["REDIS_URL"] = os.getenv("REDIS_URL", "redis://localhost:6379")

from app.job_store import init_db

init_db()


redis_conn = redis.from_url(app.config["REDIS_URL"])

q = Queue(connection=redis_conn)

from app import routes
