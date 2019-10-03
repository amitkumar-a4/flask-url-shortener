from flask import Flask

def init_app(app: Flask):
    """ Register blueprints """
    from .health import health_blueprint
    app.register_blueprint(health_blueprint)
