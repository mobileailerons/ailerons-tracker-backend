""" Custom exception classes. """

class CloudinaryError(Exception):
    """ Generic Cloudinary error """
    def __init__(self):
        self.message = "Something went wrong when uploading to Cloudinary"

class ImageNameError(Exception):
    """ Invalid image_name preventing image_id generation """
    def __init__(self, image_name:str):
        self.message = f"Could not parse image_name: {image_name}"

class InvalidFileName(Exception):
    """ Invalid file name """
    def __init__(self):
        self.message = "Invalid file name. Must not be an empty string ('')"

