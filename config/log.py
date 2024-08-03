import logging
from datetime import datetime
import pytz

def setup():
    logging.basicConfig(
        format='%(asctime)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.StreamHandler()
        ]
    )
    logging.info("logging config setup")

def _info(msg):
    logging.info(msg)

def _error(msg):
    logging.error(msg)

