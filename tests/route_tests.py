""" Test suite for image upload """

from pathlib import Path
import pytest
from ailerons_tracker_backend import errors
from ailerons_tracker_backend.clients import cloudinary_client

resources = Path(__file__).parent / "resources"


def test_client(client):
    """ Test if conf file provides client for mocking API requests """
    assert client


class TestUploadImage():
    """ Test upload"""

    def test_invalid_filename(self):
        """ With invalid filename """

        with pytest.raises(errors.ImageNameError):
            cloudinary_client.upload_image(
                'test', (resources / "test.png").open("rb"))

    def test_valid_filename(self):
        """ With valid filename but invalid path """

        with pytest.raises(FileNotFoundError):
            cloudinary_client.upload_image("test.png", "./test.png")

    def test_valid(self):
        """ valid request """

        r = cloudinary_client.upload_image(
            "test.png", (resources / "test.png").open("rb"))
        assert r


def test_news_route(client):
    """ Test news route by mocking a request """

    response = client.post("/news", data={"file": {
        "newsImage": (resources / "test.png").open("rb"),
    }, "form": {
        "newsTitle": "Fermentum leo vel orci porta non pulvinar.",
        "newsContent": "Lorem ipsum dolor sit amet",
        "newsDate": "2017-06-01T08:30"},
    })

    assert response


def test_individual_route(client):
    """ Test individual route by mocking a request """

    response = client.post("/individual", data={"file": {
        "indImage": (resources / "test.png").open("rb"),
    }, "form": {
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
        'parasites': False},
    })

    assert response


def test_upload_route(client):
    """ Test upload route by mocking a request """

    response = client.post(
        "/upload", data={"file": (resources / "data_test.csv")})

    assert response
