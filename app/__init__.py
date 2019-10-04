from flask import Flask

def create_app():
    """
    Creates an application instance to run
    :return: A Flask object
    """
    app = Flask(__name__)
    app.config.from_object('config.Base')
    register_blueprints(app)
    return app

def register_blueprints(app: Flask):
    """ Register blueprints """
    from .short_urls.routes import short_urls_bp
    from .health.routes import health_bp
    app.register_blueprint(short_urls_bp)
    app.register_blueprint(health_bp)
