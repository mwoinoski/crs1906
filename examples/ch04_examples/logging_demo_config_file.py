"""logging_demo_config_file.py - Demo of logging configuration from a
configuration file, from Chapter 4"""

import time
import shutil

import logging
import logging.config


# Load logging configuration from logging.conf.
# This only needs to be done once in the application, so it can be done in a
# top-level package's __init__.py file
logging.config.fileConfig('logging.conf')

logger = logging.getLogger('logging_demo')

# Logger handlers and message formats are configured in the config file

logger.debug('Module name = %s', __name__)

logger.info('Program started at %s', time.strftime('%X %x'))

(total, used, free) = shutil.disk_usage('/')
logger.warning('Root dir is %d%% full', 100*used/total)
