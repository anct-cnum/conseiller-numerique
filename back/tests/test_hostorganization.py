from django.core import mail
from django.test import TestCase

from tests.factories import CoachFactory


class HostOrganizationTestCase(TestCase):
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
            'zip_code': '33100',
            'start_date': '2020-11-15',
            'contact_first_name': 'Paul',
            'contact_last_name': 'Dupont',
            'contact_job': 'Directeur',
            'contact_email': 'paul.dupont@example.com',
            'contact_phone': '01 99 00 28 35',
        }

        res = self.client.post('/api/hostorganizations.add', data=data)

        self.assertEqual(201, res.status_code)
        res_data = res.json()
        del res_data['created']
        del res_data['updated']
        self.assertEqual(
            {'type': 'COMMUNE', 'has_candidate': False, 'start_date': '2020-11-15', 'name': 'Amazing Organization',
             'zip_code': '33100', 'contact_first_name': 'Paul', 'contact_last_name': 'Dupont',
             'contact_job': 'Directeur', 'contact_email': 'paul.dupont@example.com', 'contact_phone': '01 99 00 28 35',
             'location': {'type': 'Point', 'coordinates': [-0.5874, 44.8572]}},
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

    def test_post_invalid_zip_code(self):

        data = {
            'type': 'COMMUNE',
            'has_candidate': False,
            'name': 'Amazing Organization',
            'zip_code': '456',
            'start_date': '2020-11-15',
            'contact_first_name': 'Paul',
            'contact_last_name': 'Dupont',
            'contact_job': 'Directeur',
            'contact_email': 'paul.dupont@example.com',
            'contact_phone': '01 99 00 28 35',
        }
        res = self.client.post('/api/hostorganizations.add', data=data)
        self.assertEqual(400, res.status_code)
        res_data = res.json()
        self.assertEqual({'zip_code': ['Code postal invalide']}, res_data)
