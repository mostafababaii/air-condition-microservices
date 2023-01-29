import abc
import time
import datetime
import requests
from django.conf import settings


class HttpClient(metaclass=abc.ABCMeta):
    def __init__(self):
        self._response = None

    @abc.abstractmethod
    def submit(self):
        pass


class AirPollutionClient(HttpClient):
    def __init__(self, lat: float, lon: float, date_string: str):
        self.lat = lat
        self.lon = lon
        self.date_string = date_string
        super().__init__()

    def submit(self):
        self._response = requests.get("http://api.openweathermap.org/data/2.5/air_pollution/history?lat={lat}&lon={lon}&start={start_timestamp}&end={end_timestamp}&appid={api_key}".format(
            lat=self.lat,
            lon=self.lon,
            start_timestamp=self.get_date_string_as_timestamp(),
            end_timestamp=self.get_end_timestamp(),
            api_key=settings.OPEN_WEATHER_API_KEY
        ))

        return self._response.json()

    def get_date_string_as_timestamp(self) -> int:
        timestamp = time.mktime(datetime.datetime.strptime(self.date_string, "%Y-%m-%d").timetuple())
        return int(timestamp)

    def get_end_timestamp(self) -> int:
        timestamp = self.get_date_string_as_timestamp()
        timestamp += 60 * 60 * 24 # One day later

        return int(timestamp)
