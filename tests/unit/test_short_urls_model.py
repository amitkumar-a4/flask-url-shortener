import datetime as dt
import pytest

from app.users.model import User
from app.short_urls.model import Url


def test_check_random_int_generator(client):
    """Check rand_int"""
    rand_int = Url.create_id()
    assert rand_int > 10000


def test_get_by_short_url(client):
    """Get url by short url."""
    user = User('url_test@test.com', 'foo')
    user.save()
    new_short_url = Url(
      long_url='http://google.com',
      user=user,
      short_id=Url.create_id())
    new_short_url.save()

    retrieved = Url.get_by_short_url(new_short_url.get_short_url())
    assert retrieved == new_short_url


def test_create_short_id(client, mocker):
    user = User('url_create_short_url@test.com', 'foo')
    user.save()
    short_url = Url(
      long_url='https://google.com',
      user=user,
      short_id=Url.create_id())
    short_url.save()
    assert short_url.short_id