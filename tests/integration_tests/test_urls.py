from http import HTTPStatus
import json

def test_short_url_creation(client):
    """ Urls endpoint test"""
    response = client.post(
            '/urls',
            data=json.dumps(dict(
                email='john_doe@gmail.com',
                url='http://google.com'
            )),
            content_type='application/json'
        )
    data = json.loads(response.data.decode())
    assert response.status_code == HTTPStatus.CREATED, 'Short URL Created'
    assert response.content_type == 'application/json', 'Improper content type'
