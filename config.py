import os
from dotenv import load_dotenv

# Load configuration from .env file
stage = os.getenv('FLASK_ENV')
if stage == 'development':
    dotenv_file = '.env.dev'
elif stage == 'test':
    dotenv_file = '.env.test'
else:
    dotenv_file = '.env.prod'

load_dotenv(dotenv_file)


class Base:
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DEBUG = os.getenv('DEBUG')
    TESTING = os.getenv('TESTING') or False
    if stage == 'development' or stage == 'test':
        SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(PROJECT_ROOT,
                                   os.getenv('SQLALCHEMY_DATABASE_URI')))
    else:
        SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
