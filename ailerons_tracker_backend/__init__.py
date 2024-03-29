""" Configuration and factory for the app """

__version__ = "0.6"

import os
import jinja_partials
from flask import Flask, request
import postgrest
from flask_cors import CORS
from ailerons_tracker_backend.models.individual_model import Individual, Context
from ailerons_tracker_backend.blueprints.portal import portal
from .upload_image import upload_image
from .errors import InvalidFile


def create_app(test_config=None):
    """ Create an instance of the app """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Enable CORS because HTMX requests are sent as "OPTIONS"
    # by modern browsers which causes CORS errors
    CORS(app)

    # Enable Jinja Partials, which allows us to render HTML fragments instead of pages,
    # kinda like components in Vue or React.
    jinja_partials.register_extensions(app)

    # Register a blueprint => blueprint routes are now active
    app.register_blueprint(portal)
    # Get a very useful log of all routes urls when running the server
    app.logger.warning(app.url_map)

    return app
