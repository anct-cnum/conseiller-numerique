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


class ObjectWithLocationModel(models.Model):
    class Meta:
        abstract = True

    # Location
    zip_code = models.CharField(max_length=10)
    commune_code = models.CharField(max_length=10)
    geo_name = models.CharField(max_length=250)
    region_code = models.CharField(max_length=10)
    departement_code = models.CharField(max_length=10)
    location = gis_models.PointField(geography=True)


class Coach(ObjectWithLocationModel):

    situation_looking = models.BooleanField()
    situation_job = models.BooleanField()
    situation_learning = models.BooleanField()
    situation_graduated = models.BooleanField()
    formation = models.CharField(max_length=200, blank=True)
    has_experience = models.BooleanField()
    max_distance = models.IntegerField()
    start_date = models.DateField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)

    # State
    email_confirmation_key = models.CharField(max_length=50, default=random_key_50, unique=True)
    email_confirmed = models.DateTimeField(null=True, blank=True)

    # Coach has been blocked by staff
    blocked = models.DateTimeField(null=True, blank=True)

    # Coach unsubscribed from the service
    unsubscribed = models.DateTimeField(null=True, blank=True)

    # EOF State

    unsubscribe_extras = models.JSONField(default=dict, blank=True)

    updated = models.DateField(auto_now=True)
    created = models.DateTimeField(default=timezone.now)

    @property
    def is_active(self):
        return (
                bool(self.email_confirmed) and
                not bool(self.blocked) and
                not bool(self.unsubscribed)
        )

    def __str__(self):
        return '{first_name} {last_name} ({zip_code})'.format(**self.__dict__)


class HostOrganization(ObjectWithLocationModel):
    class Type(models.TextChoices):
        COMMUNE = 'COMMUNE', 'Commune'
        DEPARTEMENT = 'DEPARTEMENT', 'Département'
        REGION = 'REGION', 'Région'
        EPCI = 'EPCI', 'EPCI'
        COLLECTIVITE = 'COLLECTIVITE', 'Collectivité'
        PRIVATE = 'PRIVATE', 'Entreprise privée'
    type = models.CharField(max_length=20, choices=Type.choices)
    has_candidate = models.BooleanField()
    start_date = models.DateField()
    name = models.CharField(max_length=250)
    contact_first_name = models.CharField(max_length=100)
    contact_last_name = models.CharField(max_length=100)
    contact_job = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)

    # State
    email_confirmation_key = models.CharField(max_length=50, default=random_key_50, unique=True)
    email_confirmed = models.DateTimeField(null=True, blank=True)

    # Structure has been validated
    validated = models.DateTimeField(null=True, blank=True)

    # Structure has been blocked by staff
    blocked = models.DateTimeField(null=True, blank=True)

    # Structure unsubscribed from the service
    unsubscribed = models.DateTimeField(null=True, blank=True)

    # EOF State

    unsubscribe_extras = models.JSONField(default=dict, blank=True)

    updated = models.DateField(auto_now=True)
    created = models.DateTimeField(default=timezone.now)

    @property
    def is_active(self):
        return (
                bool(self.email_confirmed) and
                not bool(self.blocked) and
                bool(self.validated) and
                not bool(self.unsubscribed)
        )

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

    @property
    def is_active(self):
        return self.coach.is_active and self.host.is_active