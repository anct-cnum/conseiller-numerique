from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from tests.factories import MatchingFactory


DEACTIVATED_MESSAGE = "Ce besoin est désactivé, aucune action n'est désormais possible"


class MatchingActionsTestCase(TestCase):
    def test_coach_accept(self):
        matching = MatchingFactory()

        res = self.client.get('/api/matchings.coach_accept/{}'.format(matching.key))

        url = settings.FRONT_URL + '/candidature/matching/{}/coach'.format(matching.key)
        self.assertRedirects(res, url, status_code=302, fetch_redirect_response=False)

        matching.refresh_from_db()
        self.assertIsNotNone(matching.coach_accepted)

    def test_coach_reject(self):
        matching = MatchingFactory()

        res = self.client.get('/api/matchings.coach_reject/{}'.format(matching.key))

        self.assertEqual(200, res.status_code)

        matching.refresh_from_db()
        self.assertIsNotNone(matching.coach_rejected)

    def test_host_accept(self):
        matching = MatchingFactory()

        res = self.client.get('/api/matchings.host_accept/{}'.format(matching.key))

        url = settings.FRONT_URL + '/candidature/matching/{}/host'.format(matching.key)
        self.assertRedirects(res, url, status_code=302, fetch_redirect_response=False)

        matching.refresh_from_db()
        self.assertIsNotNone(matching.host_accepted)

    def test_host_reject(self):
        matching = MatchingFactory()

        res = self.client.get('/api/matchings.host_reject/{}'.format(matching.key))

        self.assertEqual(200, res.status_code)

        matching.refresh_from_db()
        self.assertIsNotNone(matching.host_rejected)

    def _assert_deactivated(self, matching, res):
        self.assertEqual(200, res.status_code)
        self.assertEqual(DEACTIVATED_MESSAGE, res.content.decode('utf8'))

        matching.refresh_from_db()
        self.assertIsNone(matching.coach_accepted)

    def test_coach_accept_deactivated(self):
        matching = MatchingFactory(host__blocked=timezone.now())
        res = self.client.get('/api/matchings.coach_accept/{}'.format(matching.key))
        self._assert_deactivated(matching, res)

    def test_coach_reject_deactivated(self):
        matching = MatchingFactory(host__blocked=timezone.now())
        res = self.client.get('/api/matchings.coach_reject/{}'.format(matching.key))
        self._assert_deactivated(matching, res)

    def test_host_accept_deactivated(self):
        matching = MatchingFactory(coach__blocked=timezone.now())
        res = self.client.get('/api/matchings.host_accept/{}'.format(matching.key))
        self._assert_deactivated(matching, res)

    def test_host_reject_deactivated(self):
        matching = MatchingFactory(coach__blocked=timezone.now())
        res = self.client.get('/api/matchings.host_reject/{}'.format(matching.key))
        self._assert_deactivated(matching, res)
