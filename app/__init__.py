from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()


def create_app():
    """
    Creates an application instance to run
    :return: A Flask object
    """
    app = Flask(__name__)
    app.config.from_object('config.Base')
    register_blueprints(app)
    register_extensions(app)
    return app


def register_blueprints(app: Flask):
    """ Register blueprints """
    from app.short_urls.routes import short_urls_bp
    from app.health.routes import health_bp
    from app.users.routes import users_bp
    from app.utils.error_handler import errors
    from app.utils.swagger import swagger_blueprint, swagger_url

    app.register_blueprint(errors)
    app.register_blueprint(short_urls_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(swagger_blueprint, url_prefix=swagger_url)


def register_extensions(app: Flask):
    JWTManager(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.commit()
