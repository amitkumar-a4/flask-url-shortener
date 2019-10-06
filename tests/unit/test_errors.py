from http import HTTPStatus


def test_missing_url(client):
    """ Missing endpoint error test"""
    response = client.get('/some-id/missing-url/')
    print('estes', response.json)
    assert response.status_code == HTTPStatus.NOT_FOUND, 'Improper response'
    assert response.json['error']
    assert response.json['code']
    assert response.json['message']
