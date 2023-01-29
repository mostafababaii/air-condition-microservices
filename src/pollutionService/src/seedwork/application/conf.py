from src.seedwork.application.types import CommandConfig, QueryConfig, EventConfig
from src.pollution.application.commands import AirPollutionCommand
from src.pollution.application.handlers import AirPollutionCommandHandler
from src.pollution.application.queries import AirPollutionQuery
from src.pollution.application.query_handlers import AirPollutionQueryHandler
from src.pollution.models import CreateAirPollutionRepository


Commands: CommandConfig = {
    AirPollutionCommand: (AirPollutionCommandHandler, CreateAirPollutionRepository)
}

Queries: QueryConfig = {
    AirPollutionQuery: AirPollutionQueryHandler
}

Events: EventConfig = {}
