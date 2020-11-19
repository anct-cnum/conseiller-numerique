from djapp.biz.matching import build_matching_host_reject_url, build_matching_host_accept_url, \
    build_matching_coach_reject_url, build_matching_coach_accept_url
from djapp.utils.emails import Email

from djapp import models


def send_coach_confirmation(coach: models.Coach):
    context = {
        'firstname': coach.first_name,
    }
    Email('confirmation_coach').send(coach.email, context)


def send_host_confirmation(host: models.HostOrganization):
    context = {
        'firstname': host.contact_first_name,
        'name': host.name,
    }
    Email('confirmation_host').send(host.contact_email, context)


def send_matching(request, matching: models.Matching):
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
        'coachaccepturl': build_matching_coach_accept_url(request, matching),
        'coachrejecturl': build_matching_coach_reject_url(request, matching),
    })
    host_context = dict(**context, **{
        'hostaccepturl': build_matching_host_accept_url(request, matching),
        'hostrejecturl': build_matching_host_reject_url(request, matching),
    })
    Email('matching_coach').send(matching.coach.email, coach_context)
    Email('matching_host').send(matching.host.contact_email, host_context)
