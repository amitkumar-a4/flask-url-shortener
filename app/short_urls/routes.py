from flask import Blueprint, abort, request, jsonify, make_response
from ..users.model import User
from .model import Url


# Declare the blueprint
short_urls_bp = Blueprint('short_urls', __name__)


# Register controller
@short_urls_bp.route('/')
def health():
    return {'message': 'OK'}


@short_urls_bp.route('/urls', methods=['POST'])
def register_url():
    # Dummy email, will be provided by jwt
    email = request.json.get('email')
    url = request.json.get('url')

    current_user = User.get_by_email(email)
    if not current_user:
        abort(400, 'account does not exist')

    # create short url
    new_short_url = Url(
      user=current_user,
      long_url=url,
      short_url=Url._rand_id())
    short_url = new_short_url.save()

    response_body = {
            "message": "Short URL Created",
            "data": short_url.to_dict()
        }
    response = make_response(jsonify(response_body), 201)
    return response
