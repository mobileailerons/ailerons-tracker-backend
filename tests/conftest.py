""" Configuration file enabling test suites to access predefined fixtures """
import pytest
from ailerons_tracker_backend import create_app


@pytest.fixture()
def app():
    """ Give tests access to a temporary instance of app """
    app = create_app({
        'TESTING': True
    })

    yield app


@pytest.fixture()
def client(app):
    """ Give test suites access to a test client for HTTP requests """
    return app.test_client()


@pytest.fixture()
def route_map(app):
    """ Gives access to a list of app routes """
    return app.url_map
