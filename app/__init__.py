from flask import Flask
import os
from rq import Queue
from flask_cors import CORS
from flask_socketio import SocketIO, emit


app = Flask(__name__)
CORS(app)
app.config["RABBITMQ_HOST"] = os.getenv(
    "RABBITMQ_HOST", "amqp://guest:guest@rabbitmq:5672//"
)
app.config["REDIS_URL"] = os.getenv("REDIS_URL", "redis://localhost:6379")


socketio = SocketIO(
    app,
    cors_allowed_origins=["http://localhost:3000"],
    message_queue=app.config["RABBITMQ_HOST"],
)

from app.job_store import init_db

init_db()

from app import routes
