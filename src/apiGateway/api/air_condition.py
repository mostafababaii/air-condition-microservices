import abc
import datetime
from typing import Dict, Optional, Union
from services.cache import CacheService
from api.message_queue import (
    Producer,
    RabbitMQQueueConfig,
    RabbitMQProducer
)
from services.cache import cache_service
from services.message_queue import get_amq_client
from settings import base as base_settings


class AirConditionPayload:
    def __init__(self, lat: float, lon: float, date_string: str):
        self.lat = lat
        self.lon = lon
        self.date_string = date_string

    @property
    def lat(self) -> Union[float, int]:
        return self._lat

    @lat.setter
    def lat(self, value: Union[float, int]):
        if not isinstance(value, (float, int)):
            raise ValueError("Incorrect latitude value type, should be instance of float or int")
        self._lat = value

    @property
    def lon(self) -> Union[float, int]:
        return self._lon

    @lon.setter
    def lon(self, value: Union[float, int]):
        if not isinstance(value, (float, int)):
            raise ValueError("Incorrect longitude value type, should be instance of float or int")
        self._lon = value

    @property
    def date_string(self) -> str:
        return self._date_string

    @date_string.setter
    def date_string(self, date_string):
        try:
            datetime.datetime.strptime(date_string, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD")
        self._date_string = date_string

    def to_dict(self) -> Dict:
        return {
            "lat": self.lat,
            "lon": self.lon,
            "date_string": self.date_string
        }


class AirConditionProxy:
    def __init__(
        self,
        payload: AirConditionPayload,
        cache_service: CacheService,
        producer: Producer
    ):
        self.payload = payload
        self.cache_service = cache_service
        self.producer = producer

    @abc.abstractmethod
    def submit(self):
        pass


class AirPollutionProxy(AirConditionProxy):
    def submit(self):
        key = "air-pollution-{lat}-{lon}-{date_string}".format(
            lat=self.payload.lat,
            lon=self.payload.lon,
            date_string=self.payload.date_string,
        )
        result = self.cache_service.setnx(key, b"{}")
        if result:
            return self.producer.publish(self.payload.to_dict())
        return self.cache_service.get(key)


def get_air_pollution(payload: AirConditionPayload) -> Optional[Dict]:
    amq_client = get_amq_client(config=base_settings.RABBITMQ_CONFIG)

    producer = RabbitMQProducer(
        amq_client,
        RabbitMQQueueConfig(
            queue="ap.air.pollution",
            routing_key="ap",
            exchange="amq.direct",
            durable=base_settings.RABBITMQ_DURABLE,
            exclusive=base_settings.RABBITMQ_EXCLUSIVE
        )
    )

    proxy = AirPollutionProxy(
        payload,
        cache_service,
        producer
    )

    return proxy.submit()
