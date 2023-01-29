from django.db import models
from src.pollution.domain.entities import AirPollution
from src.pollution.domain.repositories import PersistAirPollutionRepository


class AirPollution(models.Model):
    query = models.JSONField(unique=True)
    body = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.email


class CreateAirPollutionRepository(PersistAirPollutionRepository):
    def persist(self, air_pollution: AirPollution):
        AirPollution.objects.create(
            query=air_pollution.query,
            body=air_pollution.body,
        )
        return AirPollution.objects.last()
