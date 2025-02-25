from flask import Flask
import os
from rq import Queue
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["REDIS_URL"] = os.getenv("REDIS_URL", "redis://localhost:6379")

from app.job_store import init_db

init_db()

from app import routes
