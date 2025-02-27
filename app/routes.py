import os
import uuid
import json
from flask import request, jsonify
from flask_socketio import SocketIO, emit
from app import app, socketio
from app.job_store import add_job, get_job
import pika
import time


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data.get("text")
    if not text:
        return jsonify({"error": "no text provided"}), 400

    job_id = str(uuid.uuid4())
    add_job(job_id)

    # Emite um status inicial via WebSocket para o frontend
    socketio.emit(
        "status", {"job_id": job_id, "status": "Job enviado. Aguardando resultado..."}
    )

    # Configuração do RabbitMQ
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
        socketio.emit("result", {"job_id": job_id, "result": json.loads(result)})
        return jsonify({"result": json.loads(result)})
    else:
        socketio.emit("status", {"job_id": job_id, "status": status})
        return jsonify({"status": status}), 202


# Para rodar o servidor Flask com WebSocket
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
