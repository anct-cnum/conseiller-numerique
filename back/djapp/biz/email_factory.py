from urllib.parse import urljoin

from django.conf import settings
from django.urls import reverse
from djapp.utils.emails import Email

from djapp import models


def send_coach_confirmation(coach: models.Coach):
    context = {
        'firstname': coach.first_name,
        'confirmurl': build_confirm_coach_url(coach),
        'unsubscribeurl': build_unsubscribe_coach_url(coach),
        'emailto': coach.email,
    }
    Email('confirmation_coach').send(coach.email, context)

def send_coach_pix(coach: models.Coach):
    context = {
        'firstname': coach.first_name,
        'pixurl': build_coach_pix_url(coach),
        'unsubscribeurl': build_unsubscribe_coach_url(coach),
        'emailto': coach.email,
    }
    Email('coach_pix').send(coach.email, context)

def send_host_confirmation(host: models.HostOrganization):
    context = {
        'contactfirstname': host.contact_first_name,
        'contactlastname': host.contact_last_name,
        'name': host.name,
        'confirmurl': build_confirm_host_url(host),
        'unsubscribeurl': build_unsubscribe_host_url(host),
        'emailto': host.contact_email,
    }
    Email('confirmation_host').send(host.contact_email, context)

def send_matching(matching: models.Matching):
    context = {
        'coachfirstname': matching.coach.first_name,
        'coachlastname': matching.coach.last_name,
        'coachmaxdistance': matching.coach.max_distance,
        'hostname': matching.host.name,
        'hostfirstname': matching.host.contact_first_name,
        'hostlastname': matching.host.contact_last_name,
        'hostzipcode': matching.host.zip_code,
        'startdate': matching.host.start_date.strftime('%d/%m/%Y'),
    }
    coach_context = dict(**context, **{
        'coachaccepturl': build_matching_coach_accept_url(matching),
        'coachrejecturl': build_matching_coach_reject_url(matching),
        'unsubscribeurl': build_unsubscribe_coach_url(matching.coach),
        'emailto': matching.coach.email,
    })
    host_context = dict(**context, **{
        'hostaccepturl': build_matching_host_accept_url(matching),
        'hostrejecturl': build_matching_host_reject_url(matching),
        'unsubscribeurl': build_unsubscribe_host_url(matching.host),
        'emailto': matching.host.contact_email,
    })
    Email('matching_coach').send(matching.coach.email, coach_context)
    Email('matching_host').send(matching.host.contact_email, host_context)

def send_voiture_balais(coach: models.Coach):
    context = {
        'firstname': coach.first_name,
        'yesurl': build_voiture_balais_url(coach, 'oui'),
        'nourl': build_voiture_balais_url(coach, 'non'),
        'emailto': coach.email,
    }
    Email('voiture_balais').send(coach.email, context)

def build_matching_coach_accept_url(matching: models.Matching):
    return urljoin(settings.SITE_URL, reverse('matching-coach-accept', kwargs={'key': matching.key}))


def build_matching_coach_reject_url(matching: models.Matching):
    return urljoin(settings.SITE_URL, reverse('matching-coach-reject', kwargs={'key': matching.key}))


def build_matching_host_accept_url(matching: models.Matching):
    return urljoin(settings.SITE_URL, reverse('matching-host-accept', kwargs={'key': matching.key}))


def build_matching_host_reject_url(matching: models.Matching):
    return urljoin(settings.SITE_URL, reverse('matching-host-reject', kwargs={'key': matching.key}))


def build_confirm_coach_url(coach: models.Coach):
    return urljoin(settings.SITE_URL, reverse('redirect-coach-confirm-email', kwargs={'key': coach.email_confirmation_key}))

def build_coach_pix_url(coach: models.Coach):
    return 'https://app.pix.fr/campagnes/SYAUCQ998?participantExternalId=' + str(coach.id)

def build_confirm_host_url(host: models.HostOrganization):
    return urljoin(settings.SITE_URL, reverse('redirect-host-confirm-email', kwargs={'key': host.email_confirmation_key}))


def build_unsubscribe_coach_url(coach: models.Coach):
    return urljoin(settings.SITE_URL, reverse('redirect-coach-unsubscribe', kwargs={'key': coach.email_confirmation_key}))


def build_unsubscribe_host_url(host: models.HostOrganization):
    return urljoin(settings.SITE_URL, reverse('redirect-host-unsubscribe', kwargs={'key': host.email_confirmation_key}))

def build_voiture_balais_url(coach: models.Coach, disponible: str):
    return urljoin(settings.SITE_URL, reverse('redirect-coach-voiture-balais', kwargs={'key': coach.email_confirmation_key, 'disponible': disponible}))
