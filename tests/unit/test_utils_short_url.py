import datetime as dt
import pytest

from app.utils.short_url import ShortURL
from app.short_urls.model import Url


def test_encode_url(client):
    """Encode int"""
    rand_int = ShortURL().encode(10002)
    assert rand_int == '2Bk'


def test_decode_url(client):
    """Decode str"""
    str = ShortURL().decode('2Bk')
    assert str == 10002


def test_decode_encode(client):
    rand_int = Url.create_id()
    encoded = ShortURL().encode(rand_int)
    assert ShortURL().decode(encoded) == rand_int
