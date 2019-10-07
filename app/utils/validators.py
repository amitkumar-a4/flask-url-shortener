from functools import wraps
from http import HTTPStatus
from flask import abort, request


def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            request.json
        except:
            abort(400, 'payload must be a valid json')
        return f(*args, **kwargs)
    return wrapper


def validate_schema(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            errors = schema().validate(request.json)
            if errors:
                abort(400, errors)
            return f(*args, **kwargs)
        return wrapper
    return decorator
