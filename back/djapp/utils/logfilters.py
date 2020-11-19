import logging
import socket
import threading

local = threading.local()


class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Store request for logs
        local.request = request
        response = self.get_response(request)
        return response


class SessionIdFilter(logging.Filter):
    def filter(self, record):
        try:
            record.session_id = local.request.session.session_key
        except AttributeError:
            record.session_id = ''
        return True


class HostnameFilter(logging.Filter):
    hostname = socket.gethostname()

    def filter(self, record):
        record.hostname = HostnameFilter.hostname
        return True
