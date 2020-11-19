import requests
from django.contrib.gis.geos import Point


class InvalidZipCode(Exception):
    def __init__(self):
        super().__init__('Code postal invalide')


class GeoGouvApi:
    def get_zipcode_info(self, zipcode):
        url = 'https://geo.api.gouv.fr/communes?codePostal={zipcode}&fields=nom,code,codesPostaux,centre,population'
        url = url.format(zipcode=zipcode)
        res = requests.get(url)
        data = res.json()
        if not data:
            raise InvalidZipCode()
        else:
            return data[0]


def compute_location_from_zip_code(zip_code):
    api = GeoGouvApi()
    data = api.get_zipcode_info(zip_code)
    return Point(x=data['centre']['coordinates'][0], y=data['centre']['coordinates'][1])
