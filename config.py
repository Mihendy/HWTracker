import os

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv('DJANGO_DEBUG').lower() == 'true'
SERVER_DOMAIN = os.getenv('SERVER_DOMAIN')
