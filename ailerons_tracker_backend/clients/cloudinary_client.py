""" Cloudinary Client """

from ailerons_tracker_backend.errors import ImageNameError

from dotenv import load_dotenv
load_dotenv()

# Must be imported after loading env-vars to properly store credentials
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary_config = cloudinary.config(secure=True)


def upload_image(image_name: str, image_path: str):
    """ Upload the image and return URL. """
    if not image_name.__contains__("."):
        raise ImageNameError(image_name)

    decomposed_str = image_name.split(".")
    image_id = decomposed_str[0]
    print(image_id)

    cloudinary.uploader.upload(image_path,
                               public_id=image_id,
                               unique_filename=False,
                               overwrite=True)

    # Build the URL for the image and save it in the variable 'srcURL'
    return cloudinary.CloudinaryImage(image_id).build_url()
