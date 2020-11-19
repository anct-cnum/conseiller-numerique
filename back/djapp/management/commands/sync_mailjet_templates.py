import os
import re

import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from djapp import models


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('token')

    def handle(self, *args, **options):
        token = options['token']
        ids = [
            ('1839650', 'confirmation_coach_body'),  # Conseiller - Confirmation
            ('1839792', 'matching_coach_body'),  # Conseiller - Matching
            ('1839724', 'confirmation_host_body'),  # Structure - Confirmation
            ('1839752', 'matching_host_body'),  # Structure - Matching
        ]
        for remote_template_id, local_template_name in ids:
            url = 'https://app.mailjet.com/passport/ipa/templates/{}/download/html'.format(remote_template_id)
            r = requests.get(url, headers={'cookie': 'mail_session={}'.format(token)})
            if not r.status_code == 200:
                raise CommandError('Cannot get template {}: {}'.format(remote_template_id, r.content))
            path = os.path.join(settings.BASE_DIR, 'djapp/templates/emails/{}.html')
            path = path.format(local_template_name)
            content = r.content.decode('utf8')\
            # Remove bottom link
            content = re.sub('Cet email a été envoyé à \[\[EMAIL_TO\]\].*désabonner</a>.', '', content)
            with open(path, 'w') as f:
                f.write(content)
        self.stdout.write('Ok.')
