from typing import Dict
from django.conf import settings
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import Q
from src.pollution.models import AirPollution


@registry.register_document
class AirPollutionDocument(Document):
    query = fields.ObjectField(
        properties={
            "lat": fields.FloatField(
                fields={"keyword": fields.KeywordField()}
            ),
            "lon": fields.FloatField(
                fields={"keyword": fields.KeywordField()}
            ),
            "date_string": fields.TextField(
                fields={"keyword": fields.KeywordField()}, analyzer="keyword"
            )
        }
    )

    data = fields.ObjectField()

    class Index:
        name = "air.pollution"
        settings = {
            "number_of_shards": settings.NUMBER_OF_SHARDS,
            "number_of_replicas": settings.NUMBER_OF_REPLICAS,
        }

    class Django:
        model = AirPollution


class ElasticsearchQueryClient:
    def __init__(self, document: Document):
        self.document = document

    def search(self):
        raise NotImplementedError


class GetAirPollutionQuery(ElasticsearchQueryClient):
    def __init__(self, lat: float, lon: float, date_string: str):
        super(GetAirPollutionQuery, self).__init__(document=AirPollutionDocument())
        self.lat = lat
        self.lon = lon
        self.date_string = date_string

    def search(self) -> Dict:
        result = self.document.search().query(
            'bool', filter=[
                Q('term', **{'query.lat.keyword': self.lat}),
                Q('term', **{'query.lon.keyword': self.lon}),
                Q('term', **{'query.date_string.keyword': self.date_string}),
            ]
        )
        return self._transform(result)

    def _transform(self, result) -> Dict:
        result = [item.data.__dict__["_d_"] for item in result]
        return result[0] if result else {}
