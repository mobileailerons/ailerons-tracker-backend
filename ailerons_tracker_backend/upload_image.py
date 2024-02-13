import os
from pathlib import Path
from ailerons_tracker_backend.clients import cloudinary_client
from ailerons_tracker_backend.errors import CloudinaryError

from ailerons_tracker_backend.errors import InvalidFile


def upload_image(image):
    """ Parse image from POST request and prepare filename and path for Cloudinary upload

    Args:
        request (API request): Request data

    Raises:
        InvalidFile: File could not be parsed 
    """
    try:
        image_name = Path(image.filename).stem

        image_path = os.path.join('./uploaded_img', image_name)
        image.save(image_path)

    except Exception as e:
        raise InvalidFile(e) from e

    try:
        if os.path.exists(image_path):
            image_url = cloudinary_client.upload(image_name, image_path)

    except CloudinaryError as e:
        raise e from e

    if image_url:
        os.remove(image_path)
        return image_url
