from djapp import models
from rest_framework import serializers


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Coach
        fields = (
            'id',
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
            'email_confirmed',
            'blocked',
            'is_active',

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
            'is_active',
            'updated',
            'created',
        )

