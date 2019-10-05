from flask import Blueprint, request, jsonify, make_response, abort

from .. import db
from .model import User

# Declare the blueprint
users_bp = Blueprint('users', __name__)


# Register controller
@users_bp.route('/users', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')

    # Raise an HTTPException with a 400 if email is already registered
    is_registered = User.get_by_email(email)
    if is_registered:
        abort(400, 'email already registered')

    User(email, password).save()

    response_body = {
            "message": "User Created",
            "data": {'email': email}
        }
    response = make_response(jsonify(response_body), 201)

    return response


@users_bp.route('/users/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    # Raise an HTTPException with a 400 if email is already registered
    current_user = User.get_by_email(email)
    if not current_user:
        abort(400, 'account does not exist')

    verify = current_user.check_password(password)

    response_body = {
            "message": "User Created",
            "data": {'verified': verify}
        }
    response = make_response(jsonify(response_body), 200)

    return response
