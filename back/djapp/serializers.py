import logging

from django.contrib.gis.geos import Point
from rest_framework import serializers
from rest_framework_gis.fields import GeometryField

from . import models
from .biz.geo_gouv_api import GeoGouvApi, InvalidCommuneCode


logger = logging.getLogger(__name__)


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Coach
        fields = (
            'situation_looking',
            'situation_job',
            'situation_learning',
            'situation_graduated',
            'formation',
            'has_experience',
            'max_distance',
            'start_date',
            'first_name',
            'last_name',
            'email',
            'phone',

            'location',
            'zip_code',
            'commune_code',
            'geo_name',
            'region_code',
            'departement_code',

            'updated',
            'created',
        )
        read_only_fields = (
            'updated',
            'created',
        )


class HostOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HostOrganization
        fields = (
            'type',
            'has_candidate',
            'start_date',
            'name',
            'contact_first_name',
            'contact_last_name',
            'contact_job',
            'contact_email',
            'contact_phone',

            'location',
            'zip_code',
            'commune_code',
            'geo_name',
            'region_code',
            'departement_code',

            'updated',
            'created',
        )
        read_only_fields = (
            'updated',
            'created',
        )


class MatchingReadSerialzier(serializers.ModelSerializer):
    coach = CoachSerializer()
    host = HostOrganizationSerializer()

    class Meta:
        model = models.Matching
        fields = (
            'key',
            'coach',
            'host',
            'coach_accepted',
            'coach_rejected',
            'host_accepted',
            'host_rejected',
            'created',
        )
        read_only_fields = (
            'created',
        )


class CoachConfirmEmailSerializer(serializers.Serializer):
    key = serializers.CharField(required=True)
