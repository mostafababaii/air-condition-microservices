from os import environ as env
from dotenv import load_dotenv
from services.message_queue import RabbitMQConfig

load_dotenv()


# Application
ENV = env["ENV"]


# Redis
REDIS_HOST = env["REDIS_HOST"]
REDIS_PORT = env["REDIS_PORT"]
REDIS_DB = env["REDIS_DB"]


# RabbitMQ
RABBITMQ_USERNAME = env["RABBITMQ_USERNAME"]
RABBITMQ_PASSWORD = env["RABBITMQ_PASSWORD"]
RABBITMQ_HOST = env["RABBITMQ_HOST"]
RABBITMQ_PORT = env["RABBITMQ_PORT"]
RABBITMQ_VHOST = env["RABBITMQ_VHOST"]
RABBITMQ_DURABLE = True
RABBITMQ_EXCLUSIVE = False

RABBITMQ_CONFIG = RabbitMQConfig(
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    username=RABBITMQ_USERNAME,
    password=RABBITMQ_PASSWORD,
    virtual_host=RABBITMQ_VHOST
)