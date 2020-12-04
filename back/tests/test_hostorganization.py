import datetime

from django.core import mail
from djapp.views import HostOrganizationConfirmEmailView
from freezegun import freeze_time
from rest_framework.test import APITestCase

from tests.factories import CoachFactory, HostOrganizationFactory, MatchingFactory, ActiveHostOrganizationFactory


class HostOrganizationTestCase(APITestCase):
    """
        - 01 99 00
        - 02 61 91
        - 03 53 01
        - 04 65 71
        - 05 36 49
        - 06 39 98
    """

    def test_post(self):
        coach = CoachFactory(situation_graduated=True, zip_code='33000', max_distance=5, start_date='2020-11-15')

        data = {
            'type': 'COMMUNE',
            'has_candidate': False,
            'name': 'Amazing Organization',
            'start_date': '2020-11-15',
            'contact_first_name': 'Paul',
            'contact_last_name': 'Dupont',
            'contact_job': 'Directeur',
            'contact_email': 'paul.dupont@example.com',
            'contact_phone': '01 99 00 28 35',

            'geo_name': 'Bordeaux',
            'commune_code': '33063',
            'zip_code': '33000',
            'location': {'type': 'Point', 'coordinates': [-0.5874, 44.8572]},
            'departement_code': '33',
            'region_code': '75',
        }

        res = self.client.post('/api/hostorganizations.add', data=data)

        self.assertEqual(201, res.status_code)
        res_data = res.json()
        del res_data['created']
        del res_data['updated']
        self.assertEqual(
            {'type': 'COMMUNE', 'has_candidate': False, 'start_date': '2020-11-15', 'name': 'Amazing Organization',
             'contact_first_name': 'Paul', 'contact_last_name': 'Dupont',
             'contact_job': 'Directeur', 'contact_email': 'paul.dupont@example.com', 'contact_phone': '01 99 00 28 35',
             'location': {'type': 'Point', 'coordinates': [-0.5874, 44.8572]}, 'geo_name': 'Bordeaux',
             'region_code': '75', 'departement_code': '33', 'zip_code': '33000', 'commune_code': '33063'},
            res_data,
        )
        #self.assertEqual(len(mail.outbox), 3)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Confirmation de l\'enregistrement de votre candidature')
        self.assertEqual(mail.outbox[0].to, [data['contact_email']])
        #self.assertEqual(mail.outbox[1].subject, 'Amazing Organization est prête à vous accueillir')
        #self.assertEqual(mail.outbox[1].to, [coach.email])
        #self.assertEqual(mail.outbox[2].subject, 'John Doe est disponible pour le poste de conseiller numérique')
        #self.assertEqual(mail.outbox[2].to, [data['contact_email']])

    def test_confirm_email(self):
        host = HostOrganizationFactory()

        data = {
            'key': host.email_confirmation_key,
        }
        res = self.client.post('/api/hostorganization.confirm_email', data=data)
        self.assertEqual(200, res.status_code)
        res_data = res.json()
        self.assertEqual({'success': True}, res_data)
        host.refresh_from_db()
        self.assertIsNotNone(host.email_confirmed)

    def test_confirm_email_fail_on_expiration(self):
        creation = datetime.datetime(2020, 8, 22)
        with freeze_time(creation):
            coach = CoachFactory()

        data = {
            'key': coach.email_confirmation_key,
        }
        with freeze_time(creation + datetime.timedelta(hours=HostOrganizationConfirmEmailView.EXPIRATION_LINK_HOURS + 1)):
            res = self.client.post('/api/hostorganization.confirm_email', data=data)
        self.assertEqual(400, res.status_code)
        self.assertEqual({'non_field_errors': ["Le lien de confirmation a expiré"]}, res.json())

    def test_unsubscribe(self):
        host = ActiveHostOrganizationFactory()
        matching = MatchingFactory(host=host)
        assert matching.is_active  # Be sure our factory output an active matching
        data = {
            'key': host.email_confirmation_key,
            'extras': {'hello': 'world'},
        }
        res = self.client.post('/api/hostorganization.unsubscribe', data=data)
        self.assertEqual(200, res.status_code)
        host.refresh_from_db()
        self.assertIsNotNone(host.unsubscribed)
        self.assertFalse(host.is_active)
        matching.refresh_from_db()
        self.assertFalse(matching.is_active)
