from http import HTTPStatus
import json


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
    assert response.json == {'email': 'john_doe@gmail.com'}, 'Improper'
    assert response.content_type == 'application/json', 'Improper content type'
