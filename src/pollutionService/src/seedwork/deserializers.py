from typing import Any
from types import ModuleType
from abc import ABC, abstractmethod
from src.seedwork.types import BuiltinType


class Deserializer(ABC):
    @abstractmethod
    def deserialize(self, obj: BuiltinType) -> Any:
        pass


class CeleryTaskDeserializer(Deserializer):
    def deserialize(self, obj: BuiltinType) -> Any:
        _class = self._get_class(obj)
        obj.pop("_module_path")
        obj.pop("_class_name")
        return _class(**obj)

    @staticmethod
    def _get_class(obj):
        module = CeleryTaskDeserializer._get_module(obj)
        return getattr(module, obj["_class_name"])

    @staticmethod
    def _get_module(obj: BuiltinType) -> ModuleType:
        return __import__(obj["_module_path"], fromlist=[""])


def deserialize_task(obj: BuiltinType) -> Any:
    deserializer = CeleryTaskDeserializer()
    return deserializer.deserialize(obj)
