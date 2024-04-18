""" Configuration and factory for the app """

__version__ = "0.6"

import os
from dotenv import load_dotenv
import jinja_partials
import flask_login
from flask import Flask, request
import postgrest
from flask_cors import CORS
from ailerons_tracker_backend.models.article_model import Article
from ailerons_tracker_backend.models.individual_model import Individual, Context
from ailerons_tracker_backend.blueprints.portal import portal
from .upload_image import upload_image
from .errors import CloudinaryError, InvalidFile
from ailerons_tracker_backend.models.user_model import User

load_dotenv()


def create_app(test_config=None):
    """ Create an instance of the app """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.getenv("APP_SECRET_KEY"),
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

    # Initialize logging manager
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user):
        app.logger.warning(user)
        if user == 'Admin':
            return User()

    @login_manager.unauthorized_handler
    def unauthorized_handler():
        return jinja_partials.render_partial("login/login_section.jinja")

    # Register a blueprint => blueprint routes are now active
    app.register_blueprint(portal)

    @app.post('/news')
    def upload_article():
        """ Parse form data and insert news article in DB """

        try:
            image_url = upload_image(request.files['newsImage'])
            article_data = Article(request.form, image_url).upload()

            return article_data, 200

        except (InvalidFile, CloudinaryError) as e:
            app.logger.error(e.message)
            return e.message, 400

        except postgrest.exceptions.APIError as e:
            app.logger.error(e.message)
            return e.message, 304

    @app.post('/individual')
    def create_individual():
        try:
            items = request.files.items(multi=True)
            image_urls = []

            for item in items:
                image_url = upload_image(item[1])

                image_urls.append(image_url)

            ind_data = Individual(
                request.form["indName"],
                request.form["indSex"],
                image_urls).upload()
            ind_id = ind_data.get('id')

            context_data = Context(ind_id, request.form).upload()

            content = {
                'message': 'Successfully uploaded new individual',
                'Individual data': ind_data,
                'Context': context_data
            }

            return content, 200

        except postgrest.exceptions.APIError as e:
            app.logger.error(e.message)
            return e.message, 304

        except InvalidFile as e:
            app.logger.error(e.message)
            return e.message, 400

    # Get a very useful log of all routes urls when running the server
    app.logger.warning(app.url_map)

    return app
