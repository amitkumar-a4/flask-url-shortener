import os
from dotenv import load_dotenv

# Load configuration from .env file
stage = os.getenv('FLASK_ENV') or 'development'
if stage == 'PROD':
    dotenv_file = '.env.prod'
elif stage == 'TEST':
    dotenv_file = '.env.test'
else:
    dotenv_file = '.env.dev'

load_dotenv(dotenv_file)


class Base:
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DEBUG = os.getenv('DEBUG')
    TESTING = os.getenv('TESTING') or False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(PROJECT_ROOT, os.getenv('SQLALCHEMY_DATABASE_URI'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
