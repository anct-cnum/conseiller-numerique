import sys
import logging

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
import ipware

from djapp.serializers import CoachSerializer, HostOrganizationSerializer, MatchingReadSerialzier
from .biz import email_factory
from .biz.matching import Matcher
from .models import Matching
from .permissions.recaptcha import ReCaptchaPermission

logger = logging.getLogger(__name__)


def home(request):
    return HttpResponse('Ok')


def process_matchings(request, matchings):
    for coach, host in matchings:
        m = Matching.objects.create(coach=coach, host=host)
        email_factory.send_matching(request, m)


class CoachAddView(APIView):
    authentication_classes = []
    permission_classes = [ReCaptchaPermission]

    def post(self, request, format=None):
        serializer = CoachSerializer(data=request.data)
        if serializer.is_valid():
            coach = serializer.save()
            email_factory.send_coach_confirmation(coach)
            matcher = Matcher()
            matchings = matcher.get_matchings_for_coach(coach)
            process_matchings(request, matchings)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HostOrganizationAddView(APIView):
    authentication_classes = []
    permission_classes = [ReCaptchaPermission]

    def post(self, request, format=None):
        serializer = HostOrganizationSerializer(data=request.data)
        if serializer.is_valid():
            host = serializer.save()
            email_factory.send_host_confirmation(host)
            matcher = Matcher()
            matchings = matcher.get_matchings_for_host(host)
            process_matchings(request, matchings)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchingGetView(RetrieveAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Matching.objects.all()
    serializer_class = MatchingReadSerialzier
    lookup_field = 'key'


def matching_coach_accept(request, key):
    matching = get_object_or_404(Matching, key=key)
    matching.coach_accepted = timezone.now()
    matching.save()
    url = settings.FRONT_URL + '/candidature/matching/{}/coach'.format(matching.key)
    return redirect(url)


def matching_coach_reject(request, key):
    matching = get_object_or_404(Matching, key=key)
    matching.coach_rejected = timezone.now()
    matching.save()
    return HttpResponse('<p>Merci de nous avoir tenu informé. Nous prenons en compte votre retour</p>')


def matching_host_accept(request, key):
    matching = get_object_or_404(Matching, key=key)
    matching.host_accepted = timezone.now()
    matching.save()
    url = settings.FRONT_URL + '/candidature/matching/{}/host'.format(matching.key)
    return redirect(url)


def matching_host_reject(request, key):
    matching = get_object_or_404(Matching, key=key)
    matching.host_rejected = timezone.now()
    matching.save()
    return HttpResponse('<p>Merci de nous avoir tenu informé. Nous prenons en compte votre retour</p>')
