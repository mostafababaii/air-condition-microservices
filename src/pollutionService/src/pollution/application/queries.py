from src.seedwork.application.interfaces import Query
from dataclasses import dataclass


@dataclass
class AirPollutionQuery(Query):
    lat: float
    lon: float
    date_string: str
