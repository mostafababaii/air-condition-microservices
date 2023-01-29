import abc
import json
from dataclasses import dataclass
from services.cache import cache_service


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


class Producer(MessageQueue, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def publish(self):
        pass


class Consumer(MessageQueue, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def listen(self):
        pass

    @staticmethod
    @abc.abstractmethod
    def callback(ch, method, properties, body):
        pass


class RabbitMQProducer(Producer):
    def publish(self, data):
        with self.client as client:
            channel = client.channel()
            channel.exchange_declare(
                exchange=self.config.exchange,
                durable=self.config.durable
            )

            result = channel.queue_declare(
                queue=self.config.queue,
                durable=self.config.durable,
                exclusive=self.config.exclusive
            )

            channel.queue_bind(
                queue=result.method.queue,
                exchange=self.config.exchange,
                routing_key=self.config.routing_key,
            )

            channel.basic_publish(
                exchange=self.config.exchange,
                routing_key=self.config.routing_key,
                body=json.dumps(data),
            )


class RabbitMQConsumer(Consumer):
    def listen(self):
        channel = self.client.channel()

        channel.exchange_declare(exchange=self.config.exchange, durable=self.config.durable)

        result = channel.queue_declare(
            queue=self.config.queue,
            durable=self.config.durable,
            exclusive=self.config.exclusive,
        )

        queue_name = result.method.queue

        channel.queue_bind(
            exchange=self.config.exchange,
            routing_key=self.config.routing_key,
            queue=queue_name,
        )

        print("[*] Waiting for data")

        channel.basic_consume(queue=queue_name, on_message_callback=self.callback)
        channel.start_consuming()

    @staticmethod
    @abc.abstractmethod
    def callback(ch, method, properties, body):
        pass


class AirPollutionConsumer(RabbitMQConsumer):
    @staticmethod
    def callback(ch, method, properties, body):
        payload = json.loads(body.decode())

        query = payload["query"]
        body = payload["body"]

        key = "air-pollution-{lat}-{lon}-{date_string}".format(
            lat=query["lat"],
            lon=query["lon"],
            date_string=query["date_string"],
        )

        cache_service.set(key, json.dumps(body))
        ch.basic_ack(delivery_tag=method.delivery_tag)
