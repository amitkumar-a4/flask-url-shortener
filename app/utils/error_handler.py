from flask import Blueprint, json
from werkzeug.exceptions import HTTPException

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(HTTPException)
def handle_exception(error):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = error.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": error.code,
        "error": error.name,
        "message": error.description,
    })
    response.content_type = "application/json"
    return response
