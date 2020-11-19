from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import Distance as D
from django.db.models import Q, F, Count
from django.urls import reverse

from djapp import models


class Matcher:
    MAX_MATCHINGS = 3

    def __init__(self):
        pass

    def get_queryset_coaches(self):
        qs = models.Coach.objects.all()
        # Filter on situation
        qs = qs.filter(Q(situation_graduated=True) | Q(has_experience=True) | Q(situation_learning=True))
        # Filter on matchings
        qs = qs.annotate(nb_matchings=Count('matchings'))
        qs = qs.filter(nb_matchings__lt=self.MAX_MATCHINGS)
        return qs

    def get_queryset_hosts(self):
        qs = models.HostOrganization.objects.all()
        # Filter on type
        qs = qs.exclude(type=models.HostOrganization.Type.PRIVATE)
        # Filter on matchings
        qs = qs.annotate(nb_matchings=Count('matchings'))
        qs = qs.filter(nb_matchings__lt=self.MAX_MATCHINGS)
        return qs

    def _matchings(self, coaches, hosts):
        res = []
        for coach in coaches:
            for host in hosts:
                if coach.start_date <= host.start_date:
                    distance = coach.location.distance(host.location)
                    if distance.km < coach.max_distance:
                        res.append((coach, host, distance.km))
        res.sort(key=lambda x: x[2])
        return res

    def get_matchings_for_coach(self, coach: models.Coach, limit=10):
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
        for host in qs_hosts[:self.MAX_MATCHINGS-coach.nb_matchings]:
            res.append((coach, host))
        return res

    def get_matchings_for_host(self, host: models.HostOrganization, limit=10):
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
        for coach in qs_coaches[:self.MAX_MATCHINGS-host.nb_matchings]:
            res.append((coach, host))
        return res


def build_matching_coach_accept_url(request, matching: models.Matching):
    return request.build_absolute_uri(reverse('matching-coach-accept', kwargs={'key': matching.key}))


def build_matching_coach_reject_url(request, matching: models.Matching):
    return request.build_absolute_uri(reverse('matching-coach-reject', kwargs={'key': matching.key}))


def build_matching_host_accept_url(request, matching: models.Matching):
    return request.build_absolute_uri(reverse('matching-host-accept', kwargs={'key': matching.key}))


def build_matching_host_reject_url(request, matching: models.Matching):
    return request.build_absolute_uri(reverse('matching-host-reject', kwargs={'key': matching.key}))
