"""logging_demo.py - Demo of logging module from Chapter 4"""

import logging
import time
import shutil


logger = logging.getLogger('logging_demo')

# Set logging level to DEBUG: all messages will be logged
logger.setLevel(logging.DEBUG)

# Log messages to a file
log_format = '%(asctime)s:%(levelname)s:%(message)s'
handler = logging.FileHandler('logging_demo.log')
handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(handler)

logger.debug('Module name = %s', __name__)

logger.info('Program started at %s', time.strftime('%X %x'))

total, used, free = shutil.disk_usage('/')
if used / total > 0.9:
    logger.warning('Root dir is %d%% full', 100*used/total)

# Set logging level to INFO: only INFO messages and higher will be logged
logger.setLevel(logging.INFO)

logger.debug('Module name = %s', __name__)
logger.info('Program started at %s', time.strftime('%X %x'))
logger.warning('Root dir is %d%% full', 100*used/total)

# Change log message format to include date and time
log_format = '%(asctime)s:%(levelname)s:%(message)s'
handler.setFormatter(logging.Formatter(log_format))

logger.info('Program started at %s', time.strftime('%X %x'))

# To send text messages, uncomment the following lines and change values
# as appropriate.

# from logging.handlers import SMTPHandler
# smtp_host = 'your.smtp.host.com'
# sender = 'you@your.host.com'
# to = '5551234567@txt.att.net'
# subj = 'Warning from python app'
# logger.addHandler(SMTPHandler(smtp_host, sender, to, subj))
# logger.warn('Better check the server')  # send text message
