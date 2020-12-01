from urllib.parse import urljoin

from django.conf import settings
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import Distance as D
from django.db.models import Q, F, Count
from django.urls import reverse

from djapp import models
from djapp.biz import email_factory


class Matcher:
    MAX_MATCHINGS = 3

    def __init__(self):
        pass

    def get_queryset_coaches(self):
        qs = models.Coach.objects.all()
        # Filter on situation
        qs = qs.filter(Q(situation_graduated=True) | Q(has_experience=True) | Q(situation_learning=True))
        # Email should be confirmed
        qs = qs.exclude(email_confirmed=None)
        # Should not be blocked
        qs = qs.filter(blocked=None)
        # Filter on matchings
        qs = qs.annotate(nb_matchings=Count('matchings'))
        qs = qs.filter(nb_matchings__lt=self.MAX_MATCHINGS)
        return qs

    def get_queryset_hosts(self):
        qs = models.HostOrganization.objects.all()
        # Filter on type
        qs = qs.exclude(type=models.HostOrganization.Type.PRIVATE)
        # Email should be confirmed
        qs = qs.exclude(email_confirmed=None)
        # Should be validated
        qs = qs.exclude(validated=None)
        # Should not be blocked
        qs = qs.filter(blocked=None)
        # Filter on matchings
        qs = qs.annotate(nb_matchings=Count('matchings'))
        qs = qs.filter(nb_matchings__lt=self.MAX_MATCHINGS)
        return qs

    def get_matchings_for_coach(self, coach: models.Coach, limit=None):
        coach = self.get_queryset_coaches().filter(pk=coach.pk).first()
        if not coach:
            return []
        qs_hosts = self.get_queryset_hosts()
        # res = self._matchings([coach], list(qs_hosts))
        qs_hosts = qs_hosts.filter(start_date__gte=coach.start_date)
        qs_hosts = qs_hosts.filter(location__dwithin=(coach.location, D(km=coach.max_distance)))
        qs_hosts = qs_hosts.annotate(distance=Distance('location', coach.location))
        qs_hosts = qs_hosts.order_by('distance')
        res = []
        if limit is None:
            limit = self.MAX_MATCHINGS - coach.nb_matchings
        for host in qs_hosts[:limit]:
            res.append((coach, host))
        return res

    def get_matchings_for_host(self, host: models.HostOrganization, limit=None):
        host = self.get_queryset_hosts().filter(pk=host.pk).first()
        if not host:
            return []
        qs_coaches = self.get_queryset_coaches()
        # res = self._matchings(list(qs_coaches), [host])
        qs_coaches = qs_coaches.filter(start_date__lte=host.start_date)
        qs_coaches = qs_coaches.filter(location__dwithin=(host.location, F('max_distance') * 1000))
        qs_coaches = qs_coaches.annotate(distance=Distance('location', host.location))
        qs_coaches = qs_coaches.order_by('distance')
        res = []
        if limit is None:
            limit = self.MAX_MATCHINGS - host.nb_matchings
        for coach in qs_coaches[:limit]:
            res.append((coach, host))
        return res

    def run_process_for_host(self, host):
        """Find matchings and send emails"""
        matchings = self.get_matchings_for_host(host)
        db_matchings = process_matchings(matchings)
        return db_matchings


def process_matchings(matchings):
    """Create Matching models and send emails"""
    db_matchings = []
    for coach, host in matchings:
        m = models.Matching.objects.create(coach=coach, host=host)
        email_factory.send_matching(m)
        db_matchings.append(m)
    return db_matchings
