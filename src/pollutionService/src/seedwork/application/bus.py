from typing import Union, Callable, List, Tuple, Type
from src.seedwork import tasks
from src.seedwork.domain import DomainEvent, Repository
from src.seedwork.application.types import CommandConfig, EventConfig, QueryConfig
from src.seedwork.application.interfaces import (
    Command,
    Query,
    Bus,
    QueryBus,
    AsyncListener,
)
from src.seedwork.application.conf import Commands, Queries, Events
from src.seedwork.serializers import serialize_task


class InMemoryBus(Bus):
    def __init__(self, commands: CommandConfig, events: EventConfig):
        self.commands = commands
        self.events = events
        self.queue: List[DomainEvent] = []
        self.async_listeners: Tuple[DomainEvent, AsyncListener, Type[Repository]] = []
        self.output = None

    def handle(self, message: Union[Command, DomainEvent]) -> Union[str, None]:
        return self._perform_handle(message)

    def _perform_handle(self, message: Union[Command, DomainEvent]) -> Union[str, None]:
        if isinstance(message, Command):
            self._handle_command(message)
        elif isinstance(message, DomainEvent):
            self._handle_event(message)
        else:
            raise

        while self.queue:
            self._perform_handle(self.queue.pop())

        return self.output

    def _handle_command(self, command: Command):
        handler, repo = self.commands[command.__class__]
        self.output = handler().handle(command, repo := repo())

    def _handle_event(self, event: DomainEvent):
        for listener_class, repo_class in self.events.get(event.__class__, []):
            l = listener_class()
            if isinstance(l, AsyncListener):
                self.async_listeners.append((event, l, repo_class()))
                continue
            l.handle(event, repo := repo_class())
            for aggregate in repo.seen():
                self.queue.extend(aggregate.pull_recorded_events())


class InMemoryQueryBus(QueryBus):
    def __init__(self, queries: QueryConfig):
        self.queries = queries

    def ask(self, query: Query):
        if query.__class__ not in self.queries:
            raise

        return self.queries[query.__class__]().handle(query)


bus = InMemoryBus(Commands, Events)

query_bus = InMemoryQueryBus(Queries)
