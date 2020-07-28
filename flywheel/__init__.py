import logging

from flywheel.settings import SENTRY_DSN, ENV
from flywheel.utils.sentry import init_sentry

logging.basicConfig(level="INFO", format='%(asctime)-15s [%(levelname)s] [%(name)-9s] %(message)s')
init_sentry(SENTRY_DSN, ENV)
