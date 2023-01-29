import abc
import json
from django.conf import settings
from src.pollution.application.message_queue import MessageQueue
from src.pollution import tasks


class Consumer(MessageQueue, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def listen(self):
        pass

    @staticmethod
    @abc.abstractmethod
    def callback(ch, method, properties, body):
        pass


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


class AirPollutionRabbitMQConsumer(RabbitMQConsumer):
    @staticmethod
    def callback(ch, method, properties, body):
        body = json.loads(body.decode())

        tasks.get_air_pollution.signature(
            (body["lat"], body["lon"], body["date_string"]),
            countdown=0,
            expires=settings.CELERY_TASK_EXPIRATION_TIME_IN_SECONDS,
        ).apply_async()

        ch.basic_ack(delivery_tag=method.delivery_tag)
