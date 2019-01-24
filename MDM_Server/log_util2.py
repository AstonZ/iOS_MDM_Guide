# coding=utf-8
import logging
import os
from datetime import datetime
from pprint import pprint

def dlog(msg):
    logging.debug(msg)
    pprint(msg)

def start_logging(title):
    today = datetime.now().strftime('%Y-%m-%d')
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
    LOG_FILE_NAME = 'logs/' + title + '_' + today + '.log'
    logging.basicConfig(filename=LOG_FILE_NAME, level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)