from api.message_queue import RabbitMQQueueConfig, AirPollutionConsumer
from api.services.message_queue import get_amq_client
from settings import base as base_settings


if __name__ == '__main__':
    amq_client = get_amq_client(config=base_settings.RABBITMQ_CONFIG)

    consumer = AirPollutionConsumer(
        amq_client,
        RabbitMQQueueConfig(
            queue="ag.air.pollution",
            routing_key="ag",
            exchange="amq.direct",
            durable=base_settings.RABBITMQ_DURABLE,
            exclusive=base_settings.RABBITMQ_EXCLUSIVE
        )
    )

    consumer.listen()
