import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv('DJANGO_DEBUG').lower() == 'true'

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

SERVER_DOMAIN = os.getenv('SERVER_DOMAIN')
