import pytest
from flask import Flask

@pytest.fixture
def app() -> Flask:
    from app import create_app
    """ Provides an instance of our Flask app """
    return create_app()