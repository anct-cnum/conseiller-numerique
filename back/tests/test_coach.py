import datetime

from django.core import mail

from djapp.models import HostOrganization
from djapp.views import CoachConfirmEmailView
from freezegun import freeze_time
from rest_framework.test import APITestCase
from tests.factories import HostOrganizationFactory, CoachFactory


class CoachTestCase(APITestCase):
    """
        - 01 99 00
        - 02 61 91
        - 03 53 01
        - 04 65 71
        - 05 36 49
        - 06 39 98
    """

    maxDiff = None

    def test_post(self):
        host = HostOrganizationFactory(type=HostOrganization.Type.COMMUNE, zip_code='33100', start_date='2020-11-20')

        data = {
            'situation_looking': False,
            'situation_job': False,
            'situation_learning': True,
            'situation_graduated': True,
            'formation': '',
            'has_experience': False,
            'max_distance': 20,
            'start_date': '2020-11-15',
            'first_name': 'Paul',
            'last_name': 'Dupont',
            'email': 'paul.dupont@example.com',
            'phone': '01 99 00 28 35',

            'geo_name': 'Bordeaux',
            'commune_code': '33063',
            'zip_code': '33000',
            'location': {'type': 'Point', 'coordinates': [-0.5874, 44.8572]},
            'departement_code': '33',
            'region_code': '75',
        }

        res = self.client.post('/api/coaches.add', data=data, format='json')

        self.assertEqual(201, res.status_code)
        res_data = res.json()
        del res_data['created']
        del res_data['updated']
        self.assertEqual(
            {'situation_looking': False, 'situation_job': False, 'situation_learning': True,
             'situation_graduated': True, 'formation': '', 'has_experience': False,
             'max_distance': 20, 'start_date': '2020-11-15', 'first_name': 'Paul', 'last_name': 'Dupont',
             'email': 'paul.dupont@example.com', 'phone': '01 99 00 28 35',
             'location': {'type': 'Point', 'coordinates': [-0.5874, 44.8572]}, 'geo_name': 'Bordeaux',
             'region_code': '75', 'departement_code': '33', 'zip_code': '33000', 'commune_code': '33063'},
            res_data,
        )
        #self.assertEqual(len(mail.outbox), 3)
        #self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Confirmation de l\'enregistrement de votre candidature')
        self.assertEqual(mail.outbox[0].to, [data['email']])
        #self.assertEqual(mail.outbox[1].subject, 'Amazing Host est prête à vous accueillir')
        #self.assertEqual(mail.outbox[1].to, [data['email']])
        #self.assertEqual(mail.outbox[2].subject, 'Paul Dupont est disponible pour le poste de conseiller numérique')
        #self.assertEqual(mail.outbox[2].to, [host.contact_email])

    def test_confirm_email(self):
        coach = CoachFactory()

        data = {
            'key': coach.email_confirmation_key,
        }
        res = self.client.post('/api/coach.confirm_email', data=data)
        self.assertEqual(200, res.status_code)
        res_data = res.json()
        self.assertEqual({'success': True}, res_data)
        coach.refresh_from_db()
        self.assertIsNotNone(coach.email_confirmed)

    def test_confirm_email_fail_on_expiration(self):
        creation = datetime.datetime(2020, 8, 22)
        with freeze_time(creation):
            coach = CoachFactory()

        data = {
            'key': coach.email_confirmation_key,
        }
        with freeze_time(creation + datetime.timedelta(hours=CoachConfirmEmailView.EXPIRATION_LINK_HOURS + 1)):
            res = self.client.post('/api/coach.confirm_email', data=data)
        self.assertEqual(400, res.status_code)
        self.assertEqual({'non_field_errors': ["Le lien de confirmation a expiré"]}, res.json())
