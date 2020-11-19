import logging
import ipware
import requests
from django.conf import settings
from rest_framework import permissions


logger = logging.getLogger(__name__)


class ReCaptchaPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if settings.TESTING:
            return True

        if request.method != 'POST':
            return True

        remote_ip, _ = ipware.get_client_ip(request)

        token = request.data.get('recaptcha', None)
        if not token:
            logger.warning('Missing recaptcha token ip=%r', remote_ip)
            return False

        r = requests.post('https://www.google.com/recaptcha/api/siteverify', {
            'response': token,
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'remoteip': remote_ip,
        })

        if r.status_code != 200:
            logger.warning('Invalid recaptcha. ip=%r code=%r msg=%r', remote_ip, r.status_code, r.content)
            return False

        check_response = r.json()

        if not check_response['success']:
            logger.warning('Invalid recaptcha. ip=%r code=%r msg=%r', remote_ip, r.status_code, r.content)
            return False

        return True
