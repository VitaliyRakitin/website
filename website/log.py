import logging

LOGGING_LEVEL = logging.DEBUG  # logging.WARNING

logging.basicConfig(
    format='[%(asctime)s.%(msecs)03d] - '
           '%(levelname)s: '
           '%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=LOGGING_LEVEL
)

logger = logging.getLogger(__name__)
