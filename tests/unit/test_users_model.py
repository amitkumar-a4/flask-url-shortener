import datetime as dt
import pytest

from app.users.model import User


def test_get_by_email(client):
    """Get user by ID."""
    user = User('foo@bar.com', 'foo')
    user.save()

    retrieved = User.get_by_email(user.email)
    assert retrieved == user


def test_created_at_defaults_to_datetime(client):
    """Test creation date."""
    user = User(email='baz@bar.com', password='bar')
    user.save()
    assert bool(user.created_at)
    assert isinstance(user.created_at, dt.datetime)


def test_password_is_not_nullable(client):
    """test that exception is raised if password is not set"""
    with pytest.raises(TypeError):
        assert User(email='foo@bar.com')


def test_check_password(client):
    """Check password."""
    user = User(email='test@bar.com', password='foobarbaz123')
    user.save()
    assert user.check_password('foobarbaz123')


def test_check_password_is_hashed(client):
    """Check password hash."""
    user = User(email='test@foobar.com', password='foobarbaz123')
    user.save()
    assert user.password[0:7] == '$argon2'
