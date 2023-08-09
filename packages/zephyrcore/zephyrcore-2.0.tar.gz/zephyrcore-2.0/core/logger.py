""" The customized logger for automation.

Examples
--------
Normal usage:

>>> from core.logger import logger
>>> logger.info('Info message')
INFO: Info message
>>> logger.warning('Warning message')
WARNING: Warning message

Setting the level:
>>> logger.setLevel(level=logging.DEBUG)  # Setting the logger to print debug logs

See Also
--------
Check the logging official page to get the supported levels and features:
https://docs.python.org/3/library/logging.html

"""
import logging


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    green = "\x1b[1;32m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# create logger with 'spam_application'
logger = logging.getLogger()
logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
sh.setFormatter(CustomFormatter())
sh.setLevel(logging.INFO)
logger.addHandler(sh)
LINE_SEPARATION_LENGTH = 80
LINE_SEPARATION = '=' * LINE_SEPARATION_LENGTH
