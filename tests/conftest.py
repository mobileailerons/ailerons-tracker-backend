""" Configuration file enabling test suites to access predefined fixtures """
from pathlib import Path
from flask import url_for
import pytest
from ailerons_tracker_backend import create_app
from ailerons_tracker_backend.models.user_model import User

# pylint: disable=locally-disabled, redefined-outer-name


@pytest.fixture()
def app():
    """ Give tests access to a temporary instance of app """
    app = create_app({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False
    })

    yield app


@pytest.fixture()
def client(app):
    """ Give test suites access to a test client for HTTP requests """
    user = User()
    return app.test_client(user=user)


@pytest.fixture()
def route_map(app):
    """ Gives access to a list of app routes """
    return app.url_map


@pytest.fixture()
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "storage_state": Path("./playwright/.auth/state.json"),
    }


@pytest.fixture()
def resources():
    return Path("./tests/resources")


