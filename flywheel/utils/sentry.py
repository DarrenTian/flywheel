import logging

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration


def init_sentry(dsn, environment, debug=False):
    if not dsn:
        return
    sentry_logging = LoggingIntegration(
        level=logging.INFO,
        event_level=logging.ERROR
    )
    sentry_sdk.init(
        dsn,
        debug=debug,
        environment=environment,
        integrations=[sentry_logging]
    )
