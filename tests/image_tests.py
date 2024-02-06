""" Test suite for image upload """

from pathlib import Path
import pytest
from ailerons_tracker_backend import errors
from ailerons_tracker_backend import cloudinary_client

resources = Path(__file__).parent / "resources"


def test_client(client):
    assert client


def test_routes(route_map):
    print(route_map)
    assert route_map


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


def test_article_model(client):
    """ Test article model """
    response = client.post("/news", data={"file": {
        "newsImage": (resources / "test.png").open("rb"),
    }, "form": {
        "newsTitle": "Fermentum leo vel orci porta non pulvinar.",
        "newsContent": "Lorem ipsum dolor sit amet",
        "newsDate": "2017-06-01T08:30", },
    })

    assert response
