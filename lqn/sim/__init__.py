"""
All simulation code should be contained in this package
"""
import logging
import logging.config

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("sim")
