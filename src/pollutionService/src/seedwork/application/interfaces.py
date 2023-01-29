from typing import Optional, Callable, Union
from pydantic import BaseModel
from src.seedwork.domain import Repository, DomainEvent


class Command(BaseModel):
    """
    A command presents a use-case.
    define your command using primitive data types like str, int, boolean, etc.
    we use pydantic.BaseModel to gain typing pros.
    consider to define data in initialization like below:

    def __init__(self, paramA: int, paramB: str, paramC: bool):
        pass
    """


class CommandHandler:
    """
    A command handler is responsible or handling a specific command,
    it acts like an orchestrator.
    usually, it brings domain objects using repositories,
    operates on them and, persist them using repositories again
    """

    def handle(self, command: Command, repo: Optional[Repository]) -> Optional[str]:
        raise NotImplementedError


class Listener(Callable):
    def __call__(self, *args, **kwargs):
        self.handle(*args, **kwargs)

    def handle(self, event: DomainEvent, repo: Optional[Repository]) -> None:
        raise NotImplementedError


class AsyncListener(Listener):
    pass


class Bus:
    """
    A command/event has no idea about its handling
    The bus is somewhat knows which handler is responsible for the command/event
    It also handles the business transaction boundary
    """

    def handle(self, command: Union[Command, DomainEvent]) -> Optional[str]:
        raise NotImplementedError


class Query:
    pass


class QueryHandler:
    def handle(self, query: Query):
        raise NotImplementedError


class QueryBus:
    def ask(self, query: Query):
        raise NotImplementedError


class ApplicationException(Exception):
    pass


class NoQueryResultException(Exception):
    pass


class QueryException(Exception):
    pass


class ModelQueryNotFound(Exception):
    pass


class ApplicationOrphanException(ApplicationException):
    pass
