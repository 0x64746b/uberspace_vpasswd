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
UBERSPACE_USER = '<YOUR USER>'

SECRET_KEY = '<REPLACE THIS WITH A SECRET, UNIQUE KEY!>'
WTF_CSRF_SECRET_KEY = '<REPLACE THIS WITH ANOTHER SECRET, UNIQUE KEY!>'

HOME = '/home/%s' % UBERSPACE_USER

LOG_FILE = '/var/www/virtual/%s/uberspace_vpasswd/fcgi.log' % UBERSPACE_USER
LOG_LEVEL = logging.DEBUG

DEBUG = True
