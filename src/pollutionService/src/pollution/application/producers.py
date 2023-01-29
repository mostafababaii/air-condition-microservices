import abc
import json
from src.pollution.application.message_queue import MessageQueue


class Producer(MessageQueue, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def publish(self):
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
