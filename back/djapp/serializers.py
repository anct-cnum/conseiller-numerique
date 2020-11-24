from rest_framework import serializers

from . import models
from .biz.geo_gouv_api import compute_location_from_zip_code, InvalidZipCode


class ZipCodeMixin:
    def validate(self, attrs):
        zip_code = attrs['zip_code']
        try:
            attrs['location'] = compute_location_from_zip_code(zip_code)
        except InvalidZipCode:
            raise serializers.ValidationError({'zip_code': 'Code postal invalide'})
        return attrs


class CoachSerializer(ZipCodeMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Coach
        fields = (
            'situation_looking',
            'situation_job',
            'situation_learning',
            'situation_graduated',
            'formation',
            'has_experience',
            'zip_code',
            'max_distance',
            'start_date',
            'first_name',
            'last_name',
            'email',
            'phone',

            'location',
            'updated',
            'created',
        )
        read_only_fields = (
            'location',
            'updated',
            'created',
        )


class HostOrganizationSerializer(ZipCodeMixin, serializers.ModelSerializer):
    class Meta:
        model = models.HostOrganization
        fields = (
            'type',
            'has_candidate',
            'start_date',
            'name',
            'zip_code',
            'contact_first_name',
            'contact_last_name',
            'contact_job',
            'contact_email',
            'contact_phone',

            'location',
            'updated',
            'created',
        )
        read_only_fields = (
            'location',
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
