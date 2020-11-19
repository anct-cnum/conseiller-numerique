from django.test import TestCase
from django.core import mail

from djapp.models import HostOrganization
from tests.factories import HostOrganizationFactory


class CoachTestCase(TestCase):
    """
        - 01 99 00
        - 02 61 91
        - 03 53 01
        - 04 65 71
        - 05 36 49
        - 06 39 98
    """

    def test_post(self):
        host = HostOrganizationFactory(type=HostOrganization.Type.COMMUNE, zip_code='33100', start_date='2020-11-20')

        data = {
            'situation_looking': False,
            'situation_job': False,
            'situation_learning': True,
            'situation_graduated': True,
            'formation': '',
            'has_experience': False,
            'zip_code': '33100',
            'max_distance': 20,
            'start_date': '2020-11-15',
            'first_name': 'Paul',
            'last_name': 'Dupont',
            'email': 'paul.dupont@example.com',
            'phone': '01 99 00 28 35',
        }

        res = self.client.post('/api/coaches.add', data=data)

        self.assertEqual(201, res.status_code)
        res_data = res.json()
        del res_data['created']
        del res_data['updated']
        self.assertEqual(
            {'situation_looking': False, 'situation_job': False, 'situation_learning': True,
             'situation_graduated': True, 'formation': '', 'has_experience': False, 'zip_code': '33100',
             'max_distance': 20, 'start_date': '2020-11-15', 'first_name': 'Paul', 'last_name': 'Dupont',
             'email': 'paul.dupont@example.com', 'phone': '01 99 00 28 35',
             'location': {'type': 'Point', 'coordinates': [-0.5874, 44.8572]}},
            res_data,
        )
        self.assertEqual(len(mail.outbox), 3)
        self.assertEqual(mail.outbox[0].subject, 'Confirmation de l\'enregistrement de votre candidature')
        self.assertEqual(mail.outbox[0].to, [data['email']])
        self.assertEqual(mail.outbox[1].subject, 'Amazing Host est prête à vous accueillir')
        self.assertEqual(mail.outbox[1].to, [data['email']])
        self.assertEqual(mail.outbox[2].subject, 'Paul Dupont est disponible pour le poste de conseiller numérique')
        self.assertEqual(mail.outbox[2].to, [host.contact_email])

    def test_post_invalid_zip_code(self):
        data = {
            'situation_looking': False,
            'situation_job': False,
            'situation_learning': True,
            'situation_graduated': False,
            'formation': '',
            'has_experience': False,
            'zip_code': '765',
            'max_distance': 20,
            'start_date': '2020-11-15',
            'first_name': 'Paul',
            'last_name': 'Dupont',
            'email': 'paul.dupont@example.com',
            'phone': '01 99 00 28 35',
        }
        res = self.client.post('/api/coaches.add', data=data)
        self.assertEqual(400, res.status_code)
        res_data = res.json()
        self.assertEqual({'zip_code': ['Code postal invalide']}, res_data)
