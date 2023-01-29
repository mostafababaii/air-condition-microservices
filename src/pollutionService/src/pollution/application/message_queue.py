from dataclasses import dataclass
from django.conf import settings
import pika


@dataclass
class RabbitMQConfig:
    host: str
    port: int
    username: str
    password: str
    virtual_host: str


@dataclass
class MessageQueueConfig:
    queue: str


@dataclass
class RabbitMQQueueConfig(MessageQueueConfig):
    routing_key: str
    exchange: str
    durable: bool
    exclusive: bool


class MessageQueue:
    def __init__(self, client, config: MessageQueueConfig):
        self.client = client
        self.config = config


def get_amq_client(config: RabbitMQConfig):
    credentials = pika.PlainCredentials(
        username=config.username, password=config.password
    )

    connection_params = pika.ConnectionParameters(
        host=config.host,
        port=config.port,
        virtual_host=config.virtual_host,
        credentials=credentials,
    )

    return pika.BlockingConnection(connection_params)


rabbitmq_default_config = RabbitMQConfig(
    host=settings.RABBITMQ_HOST,
    port=settings.RABBITMQ_PORT,
    username=settings.RABBITMQ_USERNAME,
    password=settings.RABBITMQ_PASSWORD,
    virtual_host=settings.RABBITMQ_VHOST
)
