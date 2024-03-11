""" Custom exception classes. """


class CloudinaryError(Exception):
    """ Generic Cloudinary error """

    def __init__(self, base_error):
        self.message = "Something went wrong while uploading images"
        self.base_error = base_error


class InvalidFile(Exception):
    """ Invalid file name """

    def __init__(self, base_error):
        self.message = "Could not parse file"
        self.base_error = base_error


class GeneratorError(Exception):
    """ Generic GeoJSON generator error """

    def __init__(self, base_error):
        self.message = "Something went wrong while generating geoJSONs"
        self.base_error = base_error


class GeneratorPointError(GeneratorError):
    """ Error building PointFeatures """

    def __init__(self, obj, base_error):
        super().__init__(base_error)
        self.message = f"Something went wrong while generating PointFeatures with {obj}"


class GeneratorLineError(GeneratorError):
    """ Invalid file name """

    def __init__(self, obj, base_error):
        super().__init__(base_error)
        self.message = f"Something went wrong while generating LineFeatures with {obj}"


class GeoJSONFileWriteError(GeneratorError):
    """ Could not create or update geoJSON file """

    def __init__(self, base_error):
        super().__init__(base_error)
        self.message = "Something went wrong while writing GeoJSON file"


class CreateRecipeError(GeneratorError):
    """ Could not create or update tileset recipe file """

    def __init__(self, base_error):
        super().__init__(base_error)
        self.message = "Something went wrong while writing recipe file"


class ParserError(Exception):
    """ Invalid file name """

    def __init__(self):
        self.message = "Something went wrong while parsing CSV file"
