from http import HTTPStatus
import json
import pytest

@pytest.mark.run(order=1)
def test_registration(client):
    """ Users endpoint test"""
    response = client.post(
            '/users',
            data=json.dumps(dict(
                email='john_doe@gmail.com',
                password='123456'
            )),
            content_type='application/json'
        )
    data = json.loads(response.data.decode())
    assert response.status_code == HTTPStatus.CREATED, 'User not registerd'
    assert response.content_type == 'application/json', 'Improper content type'


def test_login(client):
    """ Users endpoint test"""
    response = client.post(
            '/users/login',
            data=json.dumps(dict(
                email='john_doe@gmail.com',
                password='123456'
            )),
            content_type='application/json'
        )
    data = json.loads(response.data.decode())
    assert response.status_code == HTTPStatus.OK, 'User not verified'
    assert response.content_type == 'application/json', 'Improper content type'
