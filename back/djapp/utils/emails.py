import time
import logging
import datetime
import re

import html2text
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone

from djapp import models


logger = logging.getLogger(__name__)



class Email:
    def __init__(self, key):
        self.key = key

    def _apply_whitelist(self, to):
        whitelist = settings.EMAIL_WHITELIST
        # Apply whitelist
        if whitelist is not None:
            whitelist = whitelist + ['@example.com']
            l = []
            for email in to:
                for allowed_email in whitelist:
                    if allowed_email == email or (allowed_email.startswith('@') and email.endswith(allowed_email)):
                        l.append(email)
                        break
                else:
                    logger.info('Skip mail %s: Not in whitelist', email)
            to = l
        return list(set(to))

    def send(self, to, context, from_email=None):
        if isinstance(to, str):
            to = [to]

        orig_to = to
        to = self._apply_whitelist(to)
        if not to:
            logger.info('Nothing to send. To: before whitelist: %s', orig_to)
            return

        # render
        subject = self.render('emails/' + self.key + '_subject.html', context)
        subject = subject.replace('\n', ' ').replace('\r', ' ').strip()
        body_html = self.render('emails/' + self.key + '_body.html', context)
        body_text = html2text.html2text(body_html)

        msg = EmailMultiAlternatives(
            subject=subject,
            from_email=from_email,
            to=to,
            body=body_text,
            reply_to=['conseiller-numerique@anct.gouv.fr'],
        )
        msg.attach_alternative(body_html, 'text/html')
        logger.info('Send email to %s, from %r, key=%r, subject: %s', to, from_email, self.key, subject)
        msg.send()

    def render(self, template_name, context):
        return render_to_string(template_name, context)
