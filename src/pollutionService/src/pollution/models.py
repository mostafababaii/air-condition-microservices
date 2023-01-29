from django.db import models
from src.pollution.domain.entities import AirPollution as AirPollutionEntity
from src.pollution.domain.repositories import PersistAirPollutionRepository


class AirPollution(models.Model):
    query = models.JSONField(unique=True)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)


class CreateAirPollutionRepository(PersistAirPollutionRepository):
    def persist(self, air_pollution: AirPollutionEntity):
        AirPollution.objects.create(
            query=air_pollution.query,
            data=air_pollution.data,
        )
        return AirPollution.objects.last()
