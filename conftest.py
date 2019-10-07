import pytest
import os


@pytest.fixture
def app():
    """ Provides an instance of our Flask app """
    from app import create_app
    return create_app()


@pytest.fixture(scope="package", autouse=True)
def cleanup():
    """ Cleanup a db once we are finished. """
    try:
        PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
        os.remove(os.path.join(PROJECT_ROOT, 'test.db'))
    except FileNotFoundError:
        pass
