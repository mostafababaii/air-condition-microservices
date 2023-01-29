from src.seedwork.application.interfaces import Command


class AirPollutionCommand(Command):
    query: dict
    body: dict
