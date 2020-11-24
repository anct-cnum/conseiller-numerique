import datetime
import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from djapp.serializers import CoachSerializer, HostOrganizationSerializer, MatchingReadSerialzier, \
    CoachConfirmEmailSerializer
from .biz import email_factory
from .models import Matching, Coach
from .permissions.recaptcha import ReCaptchaPermission

logger = logging.getLogger(__name__)


def home(request):
    return HttpResponse('Ok')


@api_view(['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
def api_maintenance(request):
    return Response({'non_field_errors': ['Site en cours de maintenance, essayez à nouveau plus tard.']},
                    status=status.HTTP_400_BAD_REQUEST)


class CoachAddView(APIView):
    authentication_classes = []
    permission_classes = [ReCaptchaPermission]

    def post(self, request, format=None):
        serializer = CoachSerializer(data=request.data)
        if serializer.is_valid():
            coach = serializer.save()
            email_factory.send_coach_confirmation(coach)
            # matcher = Matcher()
            # matchings = matcher.get_matchings_for_coach(coach)
            # process_matchings(request, matchings)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoachConfirmEmailView(APIView):
    authentication_classes = []
    permission_classes = []
    EXPIRATION_LINK_HOURS = 120  # confirmation email is 120 hours (5 days)

    def post(self, request, format=None):
        serializer = CoachConfirmEmailSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            now = timezone.now()
            expiration_time = now - datetime.timedelta(hours=self.EXPIRATION_LINK_HOURS)
            coach = Coach.objects.filter(email_confirmation_key=data['key'], created__gte=expiration_time).first()
            if coach is None:
                return Response({'non_field_errors': ["Le lien de confirmation a expiré"]}, status=status.HTTP_400_BAD_REQUEST)
            logger.info('Confirm email %s for coach %s', coach.email, coach.pk)
            coach.email_confirmed = now
            coach.save()
            return Response({'success': True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HostOrganizationAddView(APIView):
    authentication_classes = []
    permission_classes = [ReCaptchaPermission]

    def post(self, request, format=None):
        serializer = HostOrganizationSerializer(data=request.data)
        if serializer.is_valid():
            host = serializer.save()
            email_factory.send_host_confirmation(host)
            # matcher = Matcher()
            # matchings = matcher.get_matchings_for_host(host)
            # process_matchings(request, matchings)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchingGetView(RetrieveAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Matching.objects.all()
    serializer_class = MatchingReadSerialzier
    lookup_field = 'key'


def confirm_email(request, key):
    EXPIRATION_LINK_HOURS = 72  # confirmation email is 72 hours
    now = timezone.now()
    expiration_time = now - datetime.timedelta(hours=EXPIRATION_LINK_HOURS)
    matching = get_object_or_404(Coach, confirm_email_key=key, created__gte=expiration_time)
    matching.email_confirmed = timezone.now()
    matching.save(update_fields=['email_confirmed'])
    url = settings.FRONT_URL + '/candidature/matching/{}/coach'.format(matching.key)
    return redirect(url)


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
