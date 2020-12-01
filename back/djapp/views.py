import datetime
import logging
from urllib.parse import urljoin

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from djapp.serializers import CoachSerializer, HostOrganizationSerializer, MatchingReadSerialzier, \
    ConfirmEmailSerializer
from .biz import email_factory
from .models import Matching, Coach, HostOrganization
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


class BaseConfirmEmailView(APIView):
    serializer_class = ConfirmEmailSerializer
    EXPIRATION_LINK_HOURS = 120  # confirmation email is 120 hours (5 days)

    def get_queryset(self):
        raise NotImplementedError

    def get_subject_email(self, subject):
        raise NotImplementedError

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            now = timezone.now()
            expiration_time = now - datetime.timedelta(hours=self.EXPIRATION_LINK_HOURS)
            subject = self.get_queryset().filter(email_confirmation_key=data['key'], created__gte=expiration_time).first()
            if subject is None:
                logger.warning('Confirm email token has expired or is invalid: %r', data['key'])
                return Response({'non_field_errors': ["Le lien de confirmation a expiré"]}, status=status.HTTP_400_BAD_REQUEST)
            logger.info('Confirm email %s for subject %s', self.get_subject_email(subject), subject.pk)
            subject.email_confirmed = now
            subject.save()
            return Response({'success': True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoachConfirmEmailView(BaseConfirmEmailView):
    def get_queryset(self):
        return Coach.objects.all()

    def get_subject_email(self, subject: Coach):
        return subject.email


class HostOrganizationConfirmEmailView(BaseConfirmEmailView):
    def get_queryset(self):
        return HostOrganization.objects.all()

    def get_subject_email(self, subject: HostOrganization):
        return subject.contact_email


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


def redirect_coach_confirm_email(request, key):
    return redirect(urljoin(settings.FRONT_URL, f'/candidature/conseiller/confirmation/email/{key}'))


def redirect_host_confirm_email(request, key):
    return redirect(urljoin(settings.FRONT_URL, f'/candidature/structure/confirmation/email/{key}'))
