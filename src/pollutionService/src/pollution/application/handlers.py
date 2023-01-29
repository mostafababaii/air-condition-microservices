from src.seedwork.application.interfaces import CommandHandler
from src.pollution.application.commands import AirPollutionCommand
from src.pollution.domain.entities import AirPollution
from src.pollution.models import CreateAirPollutionRepository


class AirPollutionCommandHandler(CommandHandler):
    def handle(self, command: AirPollutionCommand, repo: CreateAirPollutionRepository):
        result = repo.persist(
            AirPollution(
                query=command.query,
                data=command.data
            )
        )

        return result
