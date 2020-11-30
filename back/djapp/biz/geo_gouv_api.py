import logging
import requests
from django.contrib.gis.geos import Point


logger = logging.getLogger(__name__)


class ApiException(Exception):
    pass


class InvalidZipCode(ApiException):
    def __init__(self):
        super().__init__('Code postal invalide')


class InvalidCommuneCode(ApiException):
    pass


class GeoGouvApi:
    FIELDS_QS = 'fields=nom,code,codesPostaux,centre,population,codeDepartement,codeRegion'

    def search_commune_by_zipcode(self, zipcode):
        url = f'https://geo.api.gouv.fr/communes?codePostal={zipcode}&{self.FIELDS_QS}'
        res = requests.get(url)
        data = res.json()
        return data

    def get_commune(self, code):
        url = f'https://geo.api.gouv.fr/communes/{code}?{self.FIELDS_QS}'
        res = requests.get(url)
        if res.status_code != 200:
            logger.error('Cannot get commune: %s - %r', res.status_code, res.content)
            raise ApiException(res.status_code)
        data = res.json()
        return data
