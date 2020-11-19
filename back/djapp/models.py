from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.crypto import get_random_string

"""
x: longitude
y: latitude
"""


def random_key_50():
    return get_random_string(50)


class User(AbstractUser):
    pass


class Coach(models.Model):

    parent = models.ForeignKey(
        'self',
        models.SET_NULL,
        null=True,
        blank=True,
    )

    situation_looking = models.BooleanField()
    situation_job = models.BooleanField()
    situation_learning = models.BooleanField()
    situation_graduated = models.BooleanField()
    formation = models.CharField(max_length=200, blank=True)
    has_experience = models.BooleanField()
    zip_code = models.CharField(max_length=10)
    max_distance = models.IntegerField()
    start_date = models.DateField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)

    # computed
    location = gis_models.PointField(geography=True)

    updated = models.DateField(auto_now=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{first_name} {last_name} ({zip_code})'.format(**self.__dict__)


class HostOrganization(models.Model):
    class Type(models.TextChoices):
        COMMUNE = 'COMMUNE', 'Commune'
        DEPARTEMENT = 'DEPARTEMENT', 'Département'
        REGION = 'REGION', 'Région'
        EPCI = 'EPCI', 'EPCI'
        COLLECTIVITE = 'COLLECTIVITE', 'Collectivité'
        PRIVATE = 'PRIVATE', 'Entreprise privée'
    type = models.CharField(max_length=20, choices=Type.choices)
    has_candidate = models.BooleanField()
    zip_code = models.CharField(max_length=10)
    start_date = models.DateField()
    name = models.CharField(max_length=250)
    contact_first_name = models.CharField(max_length=100)
    contact_last_name = models.CharField(max_length=100)
    contact_job = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)

    # computed
    location = gis_models.PointField(geography=True)

    updated = models.DateField(auto_now=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '{name} ({zip_code})'.format(**self.__dict__)


class Matching(models.Model):
    key = models.CharField(max_length=50, default=random_key_50, unique=True)
    coach = models.ForeignKey(
        Coach,
        models.CASCADE,
        related_name='matchings',
        related_query_name='matchings',
    )
    host = models.ForeignKey(
        HostOrganization,
        models.CASCADE,
        related_name='matchings',
        related_query_name='matchings',
    )

    coach_accepted = models.DateTimeField(null=True, blank=True)
    coach_rejected = models.DateTimeField(null=True, blank=True)
    host_accepted = models.DateTimeField(null=True, blank=True)
    host_rejected = models.DateTimeField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
