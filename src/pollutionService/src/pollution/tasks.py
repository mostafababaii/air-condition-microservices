from project.celery import app
from src.pollution.application.clients import AirPollutionClient
from src.pollution.application.queries import AirPollutionQuery
from src.pollution.application.commands import AirPollutionCommand
from src.pollution.application.producers import RabbitMQProducer
from src.pollution.application.message_queue import (
    RabbitMQQueueConfig,
    get_amq_client,
    rabbitmq_default_config
)
from src.seedwork.application.bus import query_bus
from src.seedwork.application.bus import bus


@app.task(name="get.air.pollution", queue="celery.queue.air.pollution")
def get_air_pollution(lat: float, lon: float, date_string: str):
    query_payload = locals()

    query = AirPollutionQuery(**query_payload)
    result = query_bus.ask(query)

    if not result:
        response = AirPollutionClient(**query_payload).submit()
        result = response["list"][0]
        command = AirPollutionCommand(query=query_payload, data=result)
        bus.handle(command)

    rabbitmq_client = get_amq_client(config=rabbitmq_default_config)

    producer = RabbitMQProducer(
        rabbitmq_client,
        RabbitMQQueueConfig(
            queue="ag.air.pollution",
            routing_key="ag",
            exchange="amq.direct",
            durable=True,
            exclusive=False,
        )
    )

    producer.publish({"query": query_payload, "data": result})
