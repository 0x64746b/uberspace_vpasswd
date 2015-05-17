# coding: utf-8

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import logging


DOMAIN = '<YOUR EMAIL DOMAIN>'
UBERSPACE_SERVER = '<YOUR UBERSPACE SERVER>'

SECRET_KEY = '<REPLACE THIS WITH A SECRET, UNIQUE KEY!>'
WTF_CSRF_SECRET_KEY = '<REPLACE THIS WITH ANOTHER SECRET, UNIQUE KEY!>'

LOG_FILE = '/var/www/virtual/<YOUR USER>/uberspace_vpasswd/fcgi.log'
LOG_LEVEL = logging.DEBUG

DEBUG = True
