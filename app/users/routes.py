from flask import Blueprint, request, jsonify, make_response, abort

from .. import db
from .model import User

# Declare the blueprint
users_bp = Blueprint('users', __name__)


# Register controller
@users_bp.route('/users', methods=['POST'])
def register():
    email = request.json.get('email')
    is_registered = User.query.filter_by(email=email).first()
    if is_registered:
        # Raise an HTTPException with a 400 if email is already registered
        abort(400, 'email already registered')
    new_user = User(
            email=email,
            password_plaintext=request.json.get('password')
        )
    db.session.add(new_user)
    db.session.commit()
    print(new_user)
    response_body = {
            "message": "User Created",
            "data": {'email': email}
        }
    response = make_response(jsonify(response_body), 201)

    return response
