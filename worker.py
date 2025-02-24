import pika, json, os, time
from app.tasks import process_text
from app.job_store import update_job

rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")

connection = None
while connection is None:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_host)
        )
    except pika.exceptions.AMQPConnectionError:
        print(
            "Não foi possível conectar ao RabbitMQ. Tentando novamente em 5 segundos..."
        )
        time.sleep(5)

channel = connection.channel()
channel.queue_declare(queue="task_queue", durable=True)


def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        job_id = data["job_id"]
        text = data["text"]
        print(f"Recebido job: {job_id} com texto: {text}")

        result = process_text(text)

        formatted_result = {"content": result, "role": "assistant", "tool_calls": None}
        update_job(job_id, json.dumps(formatted_result))

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Job {job_id} processado.")
    except Exception as e:
        print("Erro no processamento do job:", e)
        ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="task_queue", on_message_callback=callback)

print("Worker iniciado. Aguardando mensagens...")
channel.start_consuming()
