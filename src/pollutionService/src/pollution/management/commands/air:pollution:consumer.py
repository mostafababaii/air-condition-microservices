from django.core.management.base import BaseCommand
from django.conf import settings
from src.pollution.application.consumers import AirPollutionRabbitMQConsumer
from src.pollution.application.message_queue import RabbitMQQueueConfig, get_amq_client, rabbitmq_default_config


class Command(BaseCommand):
    def handle(self, *args, **options):
        amq_client = get_amq_client(config=rabbitmq_default_config)

        consumer = AirPollutionRabbitMQConsumer(
            amq_client,
            RabbitMQQueueConfig(
                queue="ap.air.pollution",
                routing_key="ap",
                exchange="amq.direct",
                durable=True,
                exclusive=False
            )
        )

        consumer.listen()
