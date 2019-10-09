from flask import Blueprint, abort, request, jsonify, make_response, redirect
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import logging
from app.utils.validators import validate_json, validate_schema
from app.users.model import User
from app.short_urls.model import Url
from app.short_urls.constants import (
  SHORT_URL_CREATED, URL_DONT_EXIST, INVALID_ACCOUNT)
from app.short_urls.schema import UrlSchema
from app.utils.helpers import create_response

# Declare the blueprint
short_urls_bp = Blueprint('short_urls', __name__)


# Register controller
@short_urls_bp.route('/urls', methods=['POST'])
@jwt_required
@validate_json
@validate_schema(UrlSchema)
def register_url():
    logging.info('Processing shorten request')
    url = request.json.get('url')
    current_user = User.get_by_email(get_jwt_identity())
    if not current_user:
        abort(HTTPStatus.BAD_REQUEST, INVALID_ACCOUNT)

    # create short url
    new_short_url = Url(
      user=current_user,
      long_url=url,
      short_id=Url.create_id())
    new_short_url.save()

    response = create_response({
              'short_url': new_short_url.get_short_url()
            }, SHORT_URL_CREATED, HTTPStatus.CREATED)

    return response


@short_urls_bp.route('/<short_url>', methods=['GET'])
def redirect_to_long_url(short_url):
    logging.info('Processing get long url request')
    url = Url.get_by_short_url(short_url)
    if not url:
        abort(HTTPStatus.NOT_FOUND, URL_DONT_EXIST)
    return redirect(url.long_url, code=HTTPStatus.PERMANENT_REDIRECT)
