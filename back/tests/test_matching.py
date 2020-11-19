from django.test import TestCase

from djapp.models import HostOrganization
from .factories import CoachFactory, HostOrganizationFactory, MatchingFactory
from djapp.biz.matching import Matcher


class CoachTestCase(TestCase):

    def test_coach_matching(self):
        coach = CoachFactory(
            situation_graduated=True,
            zip_code='75013',
            max_distance=5,
            start_date='2020-11-15',
        )

        host1 = HostOrganizationFactory(type=HostOrganization.Type.COMMUNE, zip_code='75015', start_date='2020-11-20')
        host2 = HostOrganizationFactory(type=HostOrganization.Type.COMMUNE, zip_code='75011', start_date='2020-11-20')
        host3 = HostOrganizationFactory(type=HostOrganization.Type.COMMUNE, zip_code='94200', start_date='2020-11-20')

        # Too far
        HostOrganizationFactory(type=HostOrganization.Type.COMMUNE, zip_code='33000', start_date='2020-11-20')
        HostOrganizationFactory(type=HostOrganization.Type.COMMUNE, zip_code='92330', start_date='2020-11-20')
        HostOrganizationFactory(type=HostOrganization.Type.COMMUNE, zip_code='94700', start_date='2020-11-20')

        # Not ready
        HostOrganizationFactory(
            type=HostOrganization.Type.COMMUNE,
            zip_code='33000',
            start_date='2021-01-01',
        )

        # Too many matchings
        host_busy = HostOrganizationFactory(type=HostOrganization.Type.COMMUNE, zip_code='75015', start_date='2020-11-20')
        for i in range(Matcher.MAX_MATCHINGS):
            MatchingFactory(host=host_busy)

        matcher = Matcher()
        matchings = matcher.get_matchings_for_coach(coach)
        self.assertEqual(
            [host1, host2, host3],
            [host for _, host in matchings],
        )

    def test_host_matching(self):
        host = HostOrganizationFactory(type=HostOrganization.Type.COMMUNE, zip_code='75013', start_date='2020-11-20')

        coach1 = CoachFactory(situation_graduated=True, zip_code='75015', max_distance=5, start_date='2020-11-15')
        coach2 = CoachFactory(has_experience=True, zip_code='75013', max_distance=5, start_date='2020-11-15')
        coach3 = CoachFactory(situation_learning=True, zip_code='94200', max_distance=5, start_date='2020-11-15')

        # Too far
        CoachFactory(situation_graduated=True, zip_code='33000', max_distance=5, start_date='2020-11-15')
        CoachFactory(situation_graduated=True, zip_code='92330', max_distance=5, start_date='2020-11-15')
        CoachFactory(situation_graduated=True, zip_code='94700', max_distance=5, start_date='2020-11-15')

        # Bad situation
        CoachFactory(situation_job=True, zip_code='75015', max_distance=5, start_date='2020-11-15')

        # Start Date does not work
        CoachFactory(situation_graduated=True, zip_code='75013', max_distance=5, start_date='2020-11-30')

        # Too many matchings
        coach_busy = CoachFactory(situation_graduated=True, zip_code='75015', max_distance=5, start_date='2020-11-15')
        for i in range(Matcher.MAX_MATCHINGS):
            MatchingFactory(coach=coach_busy)

        matcher = Matcher()
        matchings = matcher.get_matchings_for_host(host)
        self.assertEqual(
            [coach1, coach2, coach3],
            [coach for coach, _ in matchings],
        )
