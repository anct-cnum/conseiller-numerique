import logging

import sqlparse

from django.conf import settings
from django.db import connections


logger = logging.getLogger(__name__)


class SqlDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        if settings.SQLDEBUG_ACTIVE:
            tot = 0
            for connection in connections.all():
                tot += len(connection.queries)
                for query in connection.queries:
                    msg = "db=%s (time=%s):\n%s"
                    args = (
                        connection.alias,
                        query['time'],
                        sqlparse.format(query['sql'], reindent=True),
                    )
                    logger.debug(msg, *args)
            logger.info("Total sql requests: %s", tot)

        return response
