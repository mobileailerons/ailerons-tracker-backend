import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from ailerons_tracker_backend.models.user_model import User
from ailerons_tracker_backend.errors import EnvVarError
import logging
load_dotenv()


def test_user():
    usr = User()
    assert User.id == 'Admin'


def test_get_login_page(client):

    headers = {'HTTP_HX-Request': 'true'}
    response = client.get('/portal/login/', headers=headers)
    logging.error(response)
    assert response.status_code == 200


def test_successful_login(client):
    pwd = os.getenv('ADMIN_PWD')

    if pwd:
        headers = {'HTTP_HX-Request': 'true'}
        response = client.post(
            '/portal/login/', data={
                'password': pwd
            }, headers=headers
        )
        assert response.status_code == 200

        return

    raise EnvVarError('ADMIN_PWD')


def test_invalid_pwd(client):
    pwd = 'not a valid pwd'
    headers = {'HTTP_HX-Request': 'true'}

    response = client.post(
        '/portal/login/', data={
            'password': pwd},
        headers=headers
    )

    assert response.status_code == 403
