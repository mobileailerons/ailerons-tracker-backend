""" Cloudinary test suite """
import os
from pathlib import Path
from ailerons_tracker_backend.clients import cloudinary_client
resources = Path(__file__).parent / "resources"

image = (resources / 'test.png').open('rb')
image_path = os.path.join(resources, 'test.png')


def test_upload():
    """ Test Cloudinary client """
    assert cloudinary_client.upload(
        'test', image_path) == 'https://res.cloudinary.com/dyuazjevh/image/upload/test'
