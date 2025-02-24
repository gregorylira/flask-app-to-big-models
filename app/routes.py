from app import app
from flask import request, jsonify
from app import q
from rq.job import Job
from app.tasks import process_text


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data["text"]
    if not text:
        return jsonify({"error": "no text provided"})
    job = q.enqueue(process_text, text)
    return jsonify({"job_id": job.get_id()})


@app.route("/result/<job_id>", methods=["GET"])
def get_result(job_id):
    try:
        job = Job.fetch(job_id, connection=q.connection)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if job.is_finished:
        return jsonify({"result": job.result})
    else:
        return jsonify({"status": job.get_status()}), 202
