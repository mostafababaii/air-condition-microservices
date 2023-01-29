from dataclasses import dataclass
import pika


@dataclass
class RabbitMQConfig:
    host: str
    port: int
    username: str
    password: str
    virtual_host: str

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
