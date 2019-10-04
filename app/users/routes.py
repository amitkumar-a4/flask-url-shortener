from flask import Blueprint, request, jsonify

from .. import db
from .model import User

# Declare the blueprint
users_bp = Blueprint('users', __name__)

# Register controller
@users_bp.route('/users', methods = ['POST'])
def register():
    email = request.json.get('email')
    new_user = User(
            email = email,
            password_plaintext = request.json.get('password')
        )
    db.session.add(new_user)
    db.session.commit()
    return (jsonify({ 'email': email }), 201)