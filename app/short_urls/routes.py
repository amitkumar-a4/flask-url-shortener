from flask import Blueprint, abort, request, jsonify, make_response, redirect
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.users.model import User
from app.short_urls.model import Url
from app.short_urls.constants import SHORT_URL_CREATED

# Declare the blueprint
short_urls_bp = Blueprint('short_urls', __name__)


# Register controller
@short_urls_bp.route('/urls', methods=['POST'])
@jwt_required
def register_url():
    url = request.json.get('url')
    current_user = User.get_by_email(get_jwt_identity())
    if not current_user:
        abort(HTTPStatus.BAD_REQUEST, 'account does not exist')

    # create short url
    new_short_url = Url(
      user=current_user,
      long_url=url,
      short_id=Url.create_id())
    new_short_url.save()

    response_body = {
            "message": SHORT_URL_CREATED,
            "data": {
              'short_url': new_short_url.get_short_url()
            }
        }
    response = make_response(jsonify(response_body), HTTPStatus.CREATED)
    return response


@short_urls_bp.route('/<short_url>', methods=['GET'])
def redirect_to_long_url(short_url):

    url = Url.get_by_short_url(short_url)
    if not url:
        abort(HTTPStatus.NOT_FOUND, 'url does not exist')
    return redirect(url.long_url, code=HTTPStatus.PERMANENT_REDIRECT)
