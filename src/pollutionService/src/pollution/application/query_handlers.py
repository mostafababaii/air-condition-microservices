from src.seedwork.application.interfaces import QueryHandler
from src.pollution.application.queries import AirPollutionQuery
from src.pollution.documents import GetAirPollutionQuery


class AirPollutionQueryHandler(QueryHandler):
    def handle(self, query: AirPollutionQuery):
        query_client = GetAirPollutionQuery(query.lat, query.lon, query.date_string)
        return query_client.search()
