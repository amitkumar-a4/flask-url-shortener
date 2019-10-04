from flask import Blueprint

# Declare the blueprint
health_bp = Blueprint('health', __name__)


# Register controller
@health_bp.route('/health/')
def health():
    return {'message': 'OK'}
