""" Custom exception classes. """

class CloudinaryError(BaseException):
    """ Generic Cloudinary error """
    def __init__(self):
        self.message = "Something went wrong when uploading to Cloudinary"

class ImageNameError(BaseException):
    """ Invalid image_name preventing image_id generation """
    def __init__(self, image_name:str):
        self.message = f"Could not parse image_name: {image_name}"
        