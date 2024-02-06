""" Configuration and factory for the app """

__version__ = "0.5"

import os
from flask import Flask, request
from werkzeug.utils import secure_filename
from supabase import create_client, Client
from ailerons_tracker_backend.models.article_model import Article
from ailerons_tracker_backend.clients.cloudinary_client import upload_image
from ailerons_tracker_backend.errors import InvalidFileName


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

    return app

    # a simple page that says hello
