from flask import Blueprint
from .model import Url


# Declare the blueprint
short_urls_bp = Blueprint('short_urls', __name__)


# Register controller
@short_urls_bp.route('/')
def health():
    return {'message': 'OK'}
