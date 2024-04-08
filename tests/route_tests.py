""" Test suite for image upload """

import logging
from pathlib import Path

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
