from abc import ABC, abstractmethod
from typing import Union, Any
from src.seedwork.types import BuiltinType
from src.seedwork.application.interfaces import AsyncListener
from src.seedwork.domain import DomainEvent, Repository


class Serializer(ABC):
    @abstractmethod
    def serialize(self, obj) -> BuiltinType:
        raise NotImplementedError


class CeleryTaskSerializer(Serializer):
    def serialize(
        self, obj: Union[AsyncListener, DomainEvent, Repository]
    ) -> BuiltinType:
        return obj.__dict__()


def serialize_task(obj: Any) -> BuiltinType:
    serializer = CeleryTaskSerializer()
    return serializer.serialize(obj)
