""" Configuration and factory for the app """

__version__ = "0.7"

import os
from flask_htmx import make_response
import postgrest
from flask_login import FlaskLoginClient
from dotenv import load_dotenv
from flask_wtf import CSRFProtect
from jinja_partials import render_partial, register_extensions
import flask_login
from flask import Flask, request
from flask_cors import CORS
from ailerons_tracker_backend.forms.login_form import LoginForm
from ailerons_tracker_backend.models.article_model import Article
from ailerons_tracker_backend.blueprints.portal import portal
from ailerons_tracker_backend.clients.cloudinary_client import upload
from ailerons_tracker_backend.models.user_model import User
from ailerons_tracker_backend.db import db
from .errors import CloudinaryError, InvalidFile

load_dotenv()


def create_app(test_config=None):
    """ Create an instance of the app """

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.getenv("APP_SECRET_KEY"),
        # URI can be found in Supabase dashboard, pwd can be reset there as well
        SQLALCHEMY_DATABASE_URI=f"postgresql://" \
        f"postgres.rddizwstjdinzyzvnuun:{os.getenv('DB_PWD')}" \
        "@aws-0-eu-central-1.pooler.supabase.com:5432/postgres")

    db.init_app(app)

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

    # Enable Cross Site Request Forgery protection in forms
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Enable Jinja Partials, which allows us to render HTML fragments instead of pages
    register_extensions(app)

    # Initialize logging manager
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    @ login_manager.user_loader
    def load_user(user):
        app.logger.info(f"Logged: {user}")
        if user == 'Admin':
            return User()

        return

    @ login_manager.unauthorized_handler
    def unauthorized_handler():
        form = LoginForm()
        return make_response(
            render_partial("login/login_section.jinja", form=form),
            push_url="/portal/login")

    app.test_client_class = FlaskLoginClient

    # Register a blueprint => blueprint routes are now active
    app.register_blueprint(portal)

    @ app.post('/news')
    def upload_article():
        """ Parse form data and insert news article in DB """

        try:
            with request.files["newsImage"].read() as img:
                image_url = upload(img.filename, img)
            article_data = Article(request.form, image_url).upload()

            return article_data, 200

        except (InvalidFile, CloudinaryError) as e:
            app.logger.error(e.message)
            return e.message, 400

        except postgrest.exceptions.APIError as e:
            app.logger.error(e.message)
            return e.message, 304

    # Get a very useful log of all routes urls when running the server
    app.logger.warning(app.url_map)

    return app
