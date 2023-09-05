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
    com_code = models.CharField(max_length=10, null=True)
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
    disponible = models.BooleanField(default=True)

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
                not bool(self.unsubscribed) and
                self.disponible
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
        GIP = 'GIP', 'GIP'
        PRIVATE = 'PRIVATE', 'Entreprise privée'
    type = models.CharField(max_length=20, choices=Type.choices)
    EMPLOYMENT_TYPE_CHOICES = [
            ('FT', 'Full Time'),
            ('PT', 'Part Time'),
            ]
    has_candidate = models.BooleanField()
    wants_coordinators = models.BooleanField(default=False)
    coordinator_type = models.CharField(max_length=2,
                                        choices=EMPLOYMENT_TYPE_CHOICES, blank=True, null=True)
    start_date = models.DateField()
    name = models.CharField(max_length=250)
    siret = models.CharField(max_length=14, null=True)
    coaches_requested = models.IntegerField(null=True)
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

    old_coach_accepted = models.DateTimeField(null=True, blank=True)
    old_coach_rejected = models.DateTimeField(null=True, blank=True)
    old_host_accepted = models.DateTimeField(null=True, blank=True)
    old_host_rejected = models.DateTimeField(null=True, blank=True)

    # ----- COACH -----
    # 1st phase : after receiving the basic informations of the matching,
    # does the coach want to contact the host ?
    coach_contact_ok = models.BooleanField(null=True, blank=True)
    coach_contact_datetime = models.DateTimeField(null=True, blank=True)
    # ----- END COACH -----

    # ----- HOST -----
    # 1st phase : after receiving the information of the coach,
    # does the host want to contact the coach ?
    host_contact_ok = models.BooleanField(null=True, blank=True)
    host_contact_datetime = models.DateTimeField(null=True, blank=True)

    # 2nd phase : after seeing the profile & contact info of the coach,
    # does the host have setup a meeting with the coach ?
    host_meeting_ok = models.BooleanField(null=True, blank=True)
    host_meeting_datetime = models.DateTimeField(null=True, blank=True)

    # 3nd phase : after meeting the candidat,
    # does the host want to recruit coach ?
    host_interview_result_ok = models.BooleanField(null=True, blank=True)
    host_interview_result_datetime = models.DateTimeField(null=True, blank=True)
    # ----- END HOST -----

    created = models.DateTimeField(auto_now_add=True)

    @property
    def is_active(self):
        return self.coach.is_active and self.host.is_active
