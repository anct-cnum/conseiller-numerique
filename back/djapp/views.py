import datetime
import logging
from urllib.parse import urljoin

from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from djapp.serializers import CoachSerializer, HostOrganizationSerializer, MatchingReadSerialzier, \
    ActionWithKeySerializer, UnsubscribePayloadSerializer, MatchingSetStateSerializer, DisponiblePayloadSerializer
from .biz import email_factory
from .biz import duplicate
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
        alreadyExist = duplicate.verify_duplicate_coach({ 'email': request.data['email'], 'zip_code': request.data['zip_code'] })
        if alreadyExist :
            return Response('Coach already created', status=status.HTTP_409_CONFLICT)
        if '@conseiller-numerique.fr' in request.data['email'] :
            return Response('Email invalid', status=status.HTTP_409_CONFLICT)
        serializer = CoachSerializer(data=request.data)
        if serializer.is_valid():
            coach = serializer.save()
            email_factory.send_coach_confirmation(coach)
            email_factory.send_coach_pix(coach)
            # matcher = Matcher()
            # matchings = matcher.get_matchings_for_coach(coach)
            # process_matchings(request, matchings)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BaseUnsubscribeView(APIView):
    serializer_class = UnsubscribePayloadSerializer

    def get_queryset(self):
        raise NotImplementedError

    def get_subject_email(self, subject):
        raise NotImplementedError

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            now = timezone.now()
            data = serializer.validated_data
            # XXX use something better, like tokenization with itsdangerous
            subject = self.get_queryset().filter(email_confirmation_key=data['key']).first()
            if subject is None:
                logger.warning('Unsubscribe email token is invalid: %r', data['key'])
                return Response({'non_field_errors': ['Le lien est invalide']}, status=status.HTTP_400_BAD_REQUEST)
            logger.info('Unsubscribe %s for subject %s', self.get_subject_email(subject), subject.pk)
            subject.unsubscribed = now
            subject.unsubscribe_extras = data['extras']
            subject.save()
            return Response({'success': True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoachUnsubscribeView(BaseUnsubscribeView):
    def get_queryset(self):
        return Coach.objects.all()

    def get_subject_email(self, subject: Coach):
        return subject.email


class HostOrganizationUnsubscribeView(BaseUnsubscribeView):
    def get_queryset(self):
        return HostOrganization.objects.all()

    def get_subject_email(self, subject: HostOrganization):
        return subject.contact_email


class BaseMatchingSetStateView(APIView):
    serializer_class = MatchingSetStateSerializer
    field = None

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            # XXX use something better, like tokenization with itsdangerous
            matching = get_object_or_404(Matching, key=data['key'])
            logger.info(f'Set {self.field} %s for matching %s', data['value'], matching.pk)
            setattr(matching, f'{self.field}_ok', data['value'])
            setattr(matching, f'{self.field}_datetime', timezone.now())
            matching.save()
            return Response({'success': True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MatchingSetMeetingView(BaseMatchingSetStateView):
    serializer_class = MatchingSetStateSerializer
    field = 'host_meeting'


class MatchingSetInterviewResultView(BaseMatchingSetStateView):
    serializer_class = MatchingSetStateSerializer
    field = 'host_interview_result'


class BaseConfirmEmailView(APIView):
    serializer_class = ActionWithKeySerializer
    EXPIRATION_LINK_HOURS = 4320  # confirmation email is 4320 hours (24%*30*65 hours =~ 6 months)

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

class CoachDisponibleView(APIView):
    serializer_class = DisponiblePayloadSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            subject = Coach.objects.all().filter(email_confirmation_key=data['key']).first()
            subject.disponible = data['disponible']
            subject.save()
            return Response({'success': True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HostOrganizationAddView(APIView):
    authentication_classes = []
    permission_classes = [ReCaptchaPermission]

    def post(self, request, format=None):
        alreadyExist = duplicate.verify_duplicate_host_organization({ 'siret': request.data['siret'], 'contact_email': request.data['contact_email'], 'zip_code': request.data['zip_code'] })
        if alreadyExist :
            return Response('Host Organisation already created', status=status.HTTP_409_CONFLICT)
        serializer = HostOrganizationSerializer(data=request.data)
        if serializer.is_valid():
            host = serializer.save()
            data = serializer.validated_data
            email_factory.send_host_confirmation(host)
            # Envoi du lien DS pour demandes de coordos
            if data.get('wants_coordinators', False):
                email_factory.send_host_coordo(host)
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

    def get_object(self):
        instance = super().get_object()
        if not instance.is_active:
            raise Http404
        return instance


def matching_coach_accept(request, key):
    matching = get_object_or_404(Matching, key=key)
    if not matching.is_active:
        return HttpResponse('Ce besoin est désactivé, aucune action n\'est désormais possible')
    matching.coach_contact_ok = True
    matching.coach_contact_datetime = timezone.now()
    matching.save()
    url = settings.FRONT_URL + '/candidature/matching/{}/coach'.format(matching.key)
    return redirect(url)


def matching_coach_reject(request, key):
    matching = get_object_or_404(Matching, key=key)
    if not matching.is_active:
        return HttpResponse('Ce besoin est désactivé, aucune action n\'est désormais possible')
    matching.coach_contact_ok = False
    matching.coach_contact_datetime = timezone.now()
    matching.save()
    return HttpResponse('<p>Merci de nous avoir tenu informé. Nous prenons en compte votre retour</p>')


def matching_host_accept(request, key):
    matching = get_object_or_404(Matching, key=key)
    if not matching.is_active:
        return HttpResponse('Ce besoin est désactivé, aucune action n\'est désormais possible')
    matching.host_contact_ok = True
    matching.host_contact_datetime = timezone.now()
    matching.save()
    url = settings.FRONT_URL + '/candidature/matching/{}/host'.format(matching.key)
    return redirect(url)


def matching_host_reject(request, key):
    matching = get_object_or_404(Matching, key=key)
    if not matching.is_active:
        return HttpResponse('Ce besoin est désactivé, aucune action n\'est désormais possible')
    matching.host_contact_ok = False
    matching.host_contact_datetime = timezone.now()
    matching.save()
    return HttpResponse('<p>Merci de nous avoir tenu informé. Nous prenons en compte votre retour</p>')


def redirect_coach_confirm_email(request, key):
    return redirect(urljoin(settings.FRONT_URL, f'/candidature/conseiller/confirmation/email/{key}'))


def redirect_host_confirm_email(request, key):
    return redirect(urljoin(settings.FRONT_URL, f'/candidature/structure/confirmation/email/{key}'))


def redirect_coach_unsubscribe(request, key):
    return redirect(urljoin(settings.FRONT_URL, f'/candidature/conseiller/unsubscribe/{key}'))


def redirect_host_unsubscribe(request, key):
    return redirect(urljoin(settings.FRONT_URL, f'/candidature/structure/unsubscribe/{key}'))

def redirect_coach_voiture_balais(request, key, disponible):
    return redirect(urljoin(settings.FRONT_URL, f'/candidature/conseiller/disponibilite/{key}/{disponible}'))
