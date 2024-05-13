""" Test suite for login route and user management """

import os
from dotenv import load_dotenv
from ailerons_tracker_backend.models.user_model import User
from ailerons_tracker_backend.errors import EnvVarError
load_dotenv()


def test_user():
    """ Test if user instatiates properly """

    usr = User()
    assert usr.id == 'Admin'


def test_get_login_page(client):
    """ Test getting the login page template """

    headers = {'HTTP_HX-Request': 'true'}
    response = client.get('/portal/login/', headers=headers)

    assert response.status_code == 200


def test_successful_login(app, client):
    """ Test login with a valid password """
    with app.app_context():
        pwd = os.getenv('ADMIN_PWD')

        if pwd:
            headers = {'HTTP_HX-Request': 'true'}
            response = client.post(
                '/portal/login/', data={
                    'password': pwd,
                }, headers=headers
            )
            assert response.status_code == 200

            return

        raise EnvVarError('ADMIN_PWD')


def test_invalid_pwd(client):
    """ Test unsuccessful login attempt """

    pwd = 'not a valid pwd'
    headers = {'HTTP_HX-Request': 'true'}

    response = client.post(
        '/portal/login/', data={
            'password': pwd},
        headers=headers
    )

    assert "Mot de passe incorrect" in response.data.decode("utf-8")
