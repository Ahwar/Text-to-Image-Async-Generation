from celery import Celery

# * BROKER_URI: Message broker to be used by Celery e.g. RabbitMQ
# * BACKEND_URI: Celery backend e.g. Redis

# Celery Worker
BROKER_URI = "amqp://localhost" #amqp is broker server
BACKEND_URI = "redis://localhost"

# app object of Celery class used to locate path of worker and broker
# identifier of worker / class name = 'celery app'
app = Celery(
    'celery_app',
    broker=BROKER_URI,
    backend=BACKEND_URI,
    include=['celery_task_app.tasks']
)
