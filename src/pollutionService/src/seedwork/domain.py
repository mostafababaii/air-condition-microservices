from typing import List
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class DomainEvent:
    pass


class AggregateRoot:
    def __init__(self):
        self._events: List[DomainEvent] = []

    def _record(self, event: DomainEvent) -> None:
        self._events.append(event)

    def pull_recorded_events(self) -> List[DomainEvent]:
        events = self._events[:]
        self._events = []
        return events


class Repository:
    pass


class ValueException(Exception):
    pass


class Url:
    def __init__(self, url: str) -> None:
        self.value = url

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value: str):
        check_url = URLValidator()
        try:
            check_url(new_value)
        except ValidationError:
            raise ValueException("url is not valid")
        self._value = new_value
