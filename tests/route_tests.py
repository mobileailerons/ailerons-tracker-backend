""" Test suite for image upload """

import logging
from pathlib import Path

from flask import render_template

resources = Path(__file__).parent / "resources"


def test_client(client):
    """ Test if conf file provides client for mocking API requests """
    assert client


def test_news_route(client):
    """ Test news route by mocking a request """

    response = client.post("/news", data={
        "newsImage": (resources / "test.png").open("rb"),
        "newsTitle": "Fermentum leo vel orci porta non pulvinar.",
        "newsContent": "Lorem ipsum dolor sit amet",
        "newsDate": "2017-06-01T08:30"
    })

    assert response.status_code in (200, 304)


def test_individual_route(client):
    """ Test individual route by mocking a request """

    response = client.post("/individual", data={
        "indImage": (resources / "test.png").open("rb"),
        'indName': 'Poupette',
        'indSex': 'female',
        'situation': 'alone',
        'indSize': 220,
        'mature': True,
        'feeding': False,
        'reproduction': False,
        'gestation': False,
        'jumping': True,
        'injured': False,
        'sick': False,
        'parasites': False
    })

    assert response.status_code in (200, 304)


def test_upload_route(client):
    """ Test upload route by mocking a request """

    response = client.post("/upload", data={
        "ind-select": 1,
        "loc_file": (resources / "test_upload_loc.csv").open("rb"),
        "depth_file": (resources / "test_upload_depth.csv").open("rb")})

    logging.error(response)
    assert response.status_code == 200


def test_portal_route(client):
    """ Test portal route """

    response = client.get("/portal")
    assert response.status_code == 308


def test_dashboard_route(client):
    """ Test dashboard route in the context of a regular request """

    response = client.get("/portal/dashboard")
    assert response.status_code == 200


def test_dashboard_route_htmx(client):
    """ Test dashboard route in the context of an htmx request """

    headers = {'HTTP_HX-Request': 'true'}
    response = client.get("/portal/dashboard", headers=headers)
    assert response.status_code == 200
