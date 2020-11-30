from django.contrib.gis.geos import Point
from django.core import mail
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
            email_confirmed='2020-01-01',
        )

        def valid_host_data(**overrides):
            default = dict(type=HostOrganization.Type.COMMUNE, zip_code='75015', start_date='2020-11-20')
            default.update(overrides)
            return default

        host1 = HostOrganizationFactory(**valid_host_data())
        host2 = HostOrganizationFactory(**valid_host_data(zip_code='75011'))
        host3 = HostOrganizationFactory(**valid_host_data(zip_code='94200'))

        # Too far
        HostOrganizationFactory(**valid_host_data(zip_code='33000'))
        HostOrganizationFactory(**valid_host_data(zip_code='92330'))
        HostOrganizationFactory(**valid_host_data(zip_code='94700'))

        # Start date does not work
        HostOrganizationFactory(**valid_host_data(start_date='2020-11-01'))

        # Too many matchings
        host_busy = HostOrganizationFactory(**valid_host_data())
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

        def valid_coach_data(**overrides):
            default = dict(
                situation_graduated=True, zip_code='75015', max_distance=5, start_date='2020-11-15',
                email_confirmed='2020-01-01',
            )
            default.update(overrides)
            return default
        coach1 = CoachFactory(**valid_coach_data())
        coach2 = CoachFactory(**valid_coach_data(situation_graduated=False, has_experience=True, zip_code='75013'))
        coach3 = CoachFactory(**valid_coach_data(situation_graduated=False, situation_learning=True, zip_code='94200'))

        # Too far
        CoachFactory(**valid_coach_data(zip_code='33000'))
        CoachFactory(**valid_coach_data(zip_code='92330'))
        CoachFactory(**valid_coach_data(zip_code='94700'))

        # Bad situation
        CoachFactory(**valid_coach_data(situation_graduated=False, situation_job=True))

        # Start Date does not work
        CoachFactory(**valid_coach_data(start_date='2020-11-30'))

        # Email not confirmed
        CoachFactory(**valid_coach_data(email_confirmed=None))

        # Blocked
        CoachFactory(**valid_coach_data(blocked='2020-01-01'))

        # Too many matchings
        coach_busy = CoachFactory(**valid_coach_data())
        for i in range(Matcher.MAX_MATCHINGS):
            MatchingFactory(coach=coach_busy)

        # Run test
        matcher = Matcher()
        matchings = matcher.get_matchings_for_host(host)
        self.assertEqual(
            [coach1, coach2, coach3],
            [coach for coach, _ in matchings],
        )

    def test_run_process_for_host(self):
        host = HostOrganizationFactory(
            name='Amazing Organization',
            type=HostOrganization.Type.COMMUNE, zip_code='33000', start_date='2020-11-15',
        )
        coach = CoachFactory(
            first_name='John', last_name='Doe',
            situation_graduated=True, zip_code='33000', max_distance=5, start_date='2020-11-15',
            email_confirmed='2020-01-01',
        )

        matcher = Matcher()
        matcher.run_process_for_host(host)

        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].subject, 'Amazing Organization est prête à vous accueillir')
        self.assertEqual(mail.outbox[0].to, [coach.email])
        self.assertEqual(mail.outbox[1].subject, 'John Doe est disponible pour le poste de conseiller numérique')
        self.assertEqual(mail.outbox[1].to, [host.contact_email])

    def test_quimper_does_not_match_with_brest(self):
        coach = CoachFactory(
            situation_graduated=True,
            geo_name='Brest',
            zip_code='29200',
            commune_code='29019',
            departement_code='29',
            region_code='53',
            location=Point([-4.5058, 48.4059]),
            start_date='2020-11-15',
            email_confirmed='2020-01-01',
        )

        host_brest = HostOrganizationFactory(
            type=HostOrganization.Type.COMMUNE,
            geo_name='Brest',
            zip_code='29200',
            commune_code='29019',
            departement_code='29',
            region_code='53',
            location=Point([-4.5058, 48.4059]),
            start_date='2020-11-20',
        )

        host_quimper = HostOrganizationFactory(
            type=HostOrganization.Type.COMMUNE,
            geo_name='Quimper',
            zip_code='75015',
            commune_code='29232',
            departement_code='29',
            region_code='53',
            location=Point([-4.0916, 47.9914]),
            start_date='2020-11-20',
        )

        # Run test
        matcher = Matcher()
        matchings = matcher.get_matchings_for_coach(coach)
        self.assertEqual(
            [host_brest],
            [host for _, host in matchings],
        )
