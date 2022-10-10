from celery import Celery


# * MODEL_PATH: Path to pickled machine learning model
# * BROKER_URI: Message broker to be used by Celery e.g. RabbitMQ
# * BACKEND_URI: Celery backend e.g. Redis


BROKER_URI = "amqp://localhost"
BACKEND_URI = "redis://localhost"

app = Celery(
    'celery_app',
    broker=BROKER_URI,
    backend=BACKEND_URI,
    include=['celery_task_app.tasks']
)
