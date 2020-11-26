from urllib.parse import urljoin

from django.conf import settings
from django.urls import reverse
from djapp.utils.emails import Email

from djapp import models


def send_coach_confirmation(coach: models.Coach):
    context = {
        'firstname': coach.first_name,
        'confirmemail': build_confirm_coach_url(coach),
    }
    Email('confirmation_coach').send(coach.email, context)


def send_host_confirmation(host: models.HostOrganization):
    context = {
        'contactfirstname': host.contact_first_name,
        'contactlastname': host.contact_first_name,
        'name': host.name,
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
    })
    host_context = dict(**context, **{
        'hostaccepturl': build_matching_host_accept_url(matching),
        'hostrejecturl': build_matching_host_reject_url(matching),
    })
    Email('matching_coach').send(matching.coach.email, coach_context)
    Email('matching_host').send(matching.host.contact_email, host_context)


def build_matching_coach_accept_url(matching: models.Matching):
    return urljoin(settings.SITE_URL, reverse('matching-coach-accept', kwargs={'key': matching.key}))


def build_matching_coach_reject_url(matching: models.Matching):
    return urljoin(settings.SITE_URL, reverse('matching-coach-reject', kwargs={'key': matching.key}))


def build_matching_host_accept_url(matching: models.Matching):
    return urljoin(settings.SITE_URL, reverse('matching-host-accept', kwargs={'key': matching.key}))


def build_matching_host_reject_url(matching: models.Matching):
    return urljoin(settings.SITE_URL, reverse('matching-host-reject', kwargs={'key': matching.key}))


def build_confirm_coach_url(coach: models.Coach):
    return urljoin(settings.FRONT_URL, f'/candidature/coach/confirm/email/{coach.email_confirmation_key}')
