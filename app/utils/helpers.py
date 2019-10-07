from flask import make_response, jsonify


def create_response(data, message, status):
    response_body = {
            'message': message,
            'data': data
        }
    response = jsonify(response_body), status
    return response
