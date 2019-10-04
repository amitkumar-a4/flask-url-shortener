import os
from dotenv import load_dotenv

# Load configuration from .env file
stage = os.getenv('FLASK_ENV') or 'dev'
if stage == 'PROD':
  dotenv_file = '.env.prod'
else:
  dotenv_file = '.env.dev'

load_dotenv(dotenv_file)

class Base:
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DEBUG = os.getenv('DEBUG')
    TESTING = os.getenv('TESTING') or False
    SQLALCHEMY_DATABASE_URI= os.getenv('SQLALCHEMY_DATABASE_URI') or 'sqlite:///' + os.path.join(PROJECT_ROOT, 'dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
