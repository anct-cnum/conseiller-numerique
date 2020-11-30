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
    def search_commune_by_zipcode(self, zipcode):
        url = 'https://geo.api.gouv.fr/communes?codePostal={zipcode}&fields=nom,code,codesPostaux,centre,population,codeDepartement,codeRegion'
        url = url.format(zipcode=zipcode)
        res = requests.get(url)
        data = res.json()
        return data

    def get_commune(self, code):
        url = 'https://geo.api.gouv.fr/communes/{code}?fields=centre,nom,code,codesPostaux,codeDepartement,codeRegion'
        url = url.format(code=code)
        res = requests.get(url)
        if res.status_code != 200:
            logger.error('Cannot get commune: %s - %r', res.status_code, res.content)
            raise ApiException(res.status_code)
        data = res.json()
        return data
