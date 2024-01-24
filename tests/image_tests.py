""" Test suite for image upload"""
import pytest
from csv_upload_backend import errors
from csv_upload_backend import cloudinary_client

class TestUploadImage():
    """ Test upload"""
    def test_invalid_filename(self):
        """ With invalid filename """
        with pytest.raises(errors.ImageNameError):
            cloudinary_client.upload_image('test', "./test.png")

    def test_valid_filename(self):
        """ With valid filename but invalid path """
        with pytest.raises(FileNotFoundError):
            cloudinary_client.upload_image("test.png", "./test.png")

