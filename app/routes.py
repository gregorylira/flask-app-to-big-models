import os, uuid, json
from flask import request, jsonify
from app import app
from app.job_store import add_job, get_job

import pika


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data.get("text")
    if not text:
        return jsonify({"error": "no text provided"}), 400

    job_id = str(uuid.uuid4())

    add_job(job_id)

    rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue="task_queue", durable=True)
    message = {"job_id": job_id, "text": text}
    channel.basic_publish(
        exchange="",
        routing_key="task_queue",
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    connection.close()

    return jsonify({"job_id": job_id})


@app.route("/result/<job_id>", methods=["GET"])
def get_result(job_id):
    job = get_job(job_id)
    if job is None:
        return jsonify({"error": "Job não encontrado"}), 404
    status, result = job
    if status == "finished":
        return jsonify({"result": json.loads(result)})
    else:
        return jsonify({"status": status}), 202
