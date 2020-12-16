from djapp import models
from rest_framework import viewsets, permissions
from . import serializers


class CoachViewSet(viewsets.ModelViewSet):
    queryset = models.Coach.objects.all()
    serializer_class = serializers.CoachSerializer
    permission_classes = [permissions.IsAdminUser]
