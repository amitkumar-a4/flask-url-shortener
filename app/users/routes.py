from flask import Blueprint, request, jsonify, make_response, abort
from http import HTTPStatus
from flask_jwt_extended import create_access_token
from app import db
from app.users.model import User
from app.users.constants import ALREADY_REGISTERED, USER_AUTHENTICATED, USER_CREATED

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
        abort(HTTPStatus.BAD_REQUEST, ALREADY_REGISTERED)

    new_user = User(email, password).save()
    access_token = create_access_token(identity=new_user.email)

    response_body = {
            'message': USER_CREATED,
            'data': {
                'email': new_user.email,
                'access_token': access_token
            }
        }
    response = make_response(jsonify(response_body), HTTPStatus.CREATED)

    return response


@users_bp.route('/users/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    # Raise an HTTPException with a 400 if email is already registered
    current_user = User.get_by_email(email)
    if not current_user:
        abort(HTTPStatus.BAD_REQUEST, 'account does not exist')

    verify = current_user.check_password(password)
    access_token = create_access_token(identity=current_user.email)
    response_body = {
            "message": USER_AUTHENTICATED,
            "data": {'access_token': access_token}
        }
    response = make_response(jsonify(response_body), HTTPStatus.OK)

    return response
