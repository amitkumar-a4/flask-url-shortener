import json
from http import HTTPStatus
from flask_jwt_extended import create_access_token


def test_short_url_creation(client):
    """ Urls registration endpoint test"""
    # get access token
    access_token = create_access_token(identity='john_doe@gmail.com')
    response = client.post(
            '/urls',
            data=json.dumps(dict(
                url='http://google.com'  # whatever url
            )),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'},  # set Auth header
        )
    json_data = json.loads(response.data.decode())
    assert response.status_code == HTTPStatus.CREATED, 'Short URL Created'
    assert response.content_type == 'application/json', 'Improper content type'
    assert 'data' in json_data
    assert 'message' in json_data
    assert 'short_url' in json_data['data']


def test_redirect_to_long_url(client):
    """ Urls registration endpoint test"""
    # get access token
    access_token = create_access_token(identity='john_doe@gmail.com')
    # create short_url
    creation = client.post(
            '/urls',
            data=json.dumps(dict(
                url='http://google.com'  # whatever url
            )),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'},  # set Auth header
        )
    creation_data = json.loads(creation.data.decode())
    url = creation_data['data']['short_url']
    # request created url
    response = client.get(
            f'/{url}',
            data=json.dumps(dict(
                url='http://google.com'  # whatever url
            )),
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'},  # set Auth header
        )
    assert response.status_code == 308, 'Permanent redirect'
