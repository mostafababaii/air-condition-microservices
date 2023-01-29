from typing import Any
from src.seedwork.domain import Repository
from src.pollution.domain.entities import AirPollution


class PersistAirPollutionRepository(Repository):
    def persist(self, air_pollution: AirPollution):
        raise NotImplementedError


class FetchAirPollutionRepository(Repository):
    def fetch(self, identifier: Any):
        raise NotImplementedError
