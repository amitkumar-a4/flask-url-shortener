from http import HTTPStatus

def test_health(client):
    """ Health endpoint test"""
    response = client.get('/health/')
    assert response.status_code == HTTPStatus.OK, 'Health check failed'
    assert response.json == {'message': 'OK'}, 'Improper response'