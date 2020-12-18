import functools

import factory
from django.contrib.gis.geos import Point
from djapp.biz.geo_gouv_api import GeoGouvApi
from factory import fuzzy
from django.utils import timezone

from djapp import models
from factory.errors import CyclicDefinitionError


_GEO_CACHE = {}


def decorate_with_geo_cache(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        key = f'{func.__name__}({args}, {kwargs}'
        if key not in _GEO_CACHE:
            _GEO_CACHE[key] = func(self, *args, **kwargs)
        return _GEO_CACHE[key]
    return wrapper


class CachedGeoGouvApi(GeoGouvApi):
    @decorate_with_geo_cache
    def get_commune(self, code):
        return super().get_commune(code)

    @decorate_with_geo_cache
    def search_commune_by_zipcode(self, zipcode):
        return super().search_commune_by_zipcode(zipcode)


def get_commune_data(commune_code):
    api = CachedGeoGouvApi()
    data = api.get_commune(commune_code)
    return {
        'commune_code': commune_code,
        'zip_code': data['codesPostaux'][0],  # Take first arbitrary
        'geo_name': data['nom'],
        'region_code': data['codeRegion'],
        'departement_code': data['codeDepartement'],
        'location': data['centre'],
    }


def compute_location_from_commune_code(commune_code):
    api = CachedGeoGouvApi()
    data = api.get_commune(commune_code)
    return Point(x=data['centre']['coordinates'][0], y=data['centre']['coordinates'][1])


def compute_location_from_zip_code(zip_code):
    api = CachedGeoGouvApi()
    data = api.search_commune_by_zipcode(zip_code)
    # Take first
    data = data[0]
    return Point(x=data['centre']['coordinates'][0], y=data['centre']['coordinates'][1])


def compute_location(instance):
    if instance.commune_code:
        return compute_location_from_commune_code(instance.commune_code)
    elif instance.zip_code:
        return compute_location_from_zip_code(instance.zip_code)
    else:
        return compute_location_from_commune_code('33063')  # Bordeaux


def compute_commune_code(instance):
    try:
        zip_code = instance.zip_code
    except CyclicDefinitionError:
        return '33063'
    else:
        api = CachedGeoGouvApi()
        data = api.search_commune_by_zipcode(zip_code)
        # Take first
        data = data[0]
        return data['code']


class CoachFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Coach

    situation_looking = False
    situation_job = False
    situation_learning = False
    situation_graduated = False
    formation = ''
    has_experience = False
    zip_code = '33000'
    commune_code = factory.LazyAttribute(compute_commune_code)
    geo_name = factory.LazyAttribute(lambda a: 'TestLoc(%s)' % a.commune_code)
    region_code = factory.LazyAttribute(lambda a: 'Reg(%s)' % a.commune_code)
    departement_code = factory.LazyAttribute(lambda a: 'Dep(%s)' % a.commune_code)
    max_distance = 10
    start_date = fuzzy.FuzzyDate(timezone.now().date())
    first_name = 'John'
    last_name = 'Doe'
    email = factory.LazyAttribute(lambda a: '{0}{1}@example.com'.format(a.first_name, a.last_name).lower())
    phone = ''

    # computed
    location = factory.LazyAttribute(compute_location)


class ActiveCoachFactory(CoachFactory):
    email_confirmed = timezone.now()


class HostOrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.HostOrganization

    type = fuzzy.FuzzyChoice([x for x, _ in models.HostOrganization.Type.choices])
    has_candidate = False
    zip_code = '33000'
    commune_code = factory.LazyAttribute(compute_commune_code)
    geo_name = factory.LazyAttribute(lambda a: 'TestLoc(%s)' % a.commune_code)
    region_code = factory.LazyAttribute(lambda a: 'Reg(%s)' % a.commune_code)
    departement_code = factory.LazyAttribute(lambda a: 'Dep(%s)' % a.commune_code)
    start_date = fuzzy.FuzzyDate(timezone.now().date())
    name = 'Amazing Host'
    contact_first_name = 'Pierre'
    contact_last_name = 'Dupont'
    contact_job = 'Directeur'
    contact_email = factory.LazyAttribute(lambda a: '{0}{1}@example.com'.format(a.contact_first_name, a.contact_last_name).lower())
    contact_phone = ''

    # computed
    location = factory.LazyAttribute(compute_location)


class ActiveHostOrganizationFactory(HostOrganizationFactory):
    email_confirmed = timezone.now()
    validated = timezone.now()


class MatchingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Matching

    coach = factory.SubFactory(ActiveCoachFactory)
    host = factory.SubFactory(ActiveHostOrganizationFactory)
