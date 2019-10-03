from flask import Flask

def create_app():
    """
    Creates an application instance to run
    :return: A Flask object
    """
    app = Flask(__name__)

    from . import api
    api.init_app(app)

    return app
