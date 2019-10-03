from flask import Blueprint

# Declare the blueprint
health_blueprint = Blueprint('health', __name__)

# Register controller
@health_blueprint.route('/health/')
def health():
    return {'message': 'OK'}