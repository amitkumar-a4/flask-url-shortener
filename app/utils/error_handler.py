from flask import Blueprint, json, Response
from werkzeug.exceptions import HTTPException

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(HTTPException)
def handle_exception(error) -> Response:
    """ Return JSON instead of HTML for HTTP errors. """
    response = error.get_response()
    # format the response
    response.data = json.dumps({
        "code": error.code,
        "error": error.name,
        "message": error.description,
    })
    response.content_type = "application/json"
    return response
