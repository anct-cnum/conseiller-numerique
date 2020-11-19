import factory
from factory import fuzzy
from django.utils import timezone

from djapp import models
from djapp.biz.geo_gouv_api import compute_location_from_zip_code


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
    max_distance = 10
    start_date = fuzzy.FuzzyDate(timezone.now().date())
    first_name = 'John'
    last_name = 'Doe'
    email = factory.LazyAttribute(lambda a: '{0}{1}@example.com'.format(a.first_name, a.last_name).lower())
    phone = ''

    # computed
    location = factory.LazyAttribute(lambda a: compute_location_from_zip_code(a.zip_code))


class HostOrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.HostOrganization

    type = fuzzy.FuzzyChoice([x for x, _ in models.HostOrganization.Type.choices])
    has_candidate = False
    zip_code = '33000'
    start_date = fuzzy.FuzzyDate(timezone.now().date())
    name = 'Amazing Host'
    contact_first_name = 'Pierre'
    contact_last_name = 'Dupont'
    contact_job = 'Directeur'
    contact_email = factory.LazyAttribute(lambda a: '{0}{1}@example.com'.format(a.contact_first_name, a.contact_last_name).lower())
    contact_phone = ''

    # computed
    location = factory.LazyAttribute(lambda a: compute_location_from_zip_code(a.zip_code))


class MatchingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Matching

    coach = factory.SubFactory(CoachFactory)
    host = factory.SubFactory(HostOrganizationFactory)
