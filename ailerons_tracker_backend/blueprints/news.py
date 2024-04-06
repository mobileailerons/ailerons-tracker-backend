""" Portal homepage blueprint """
import flask_login
import postgrest
from flask import Blueprint, render_template, abort, request, current_app
from jinja2 import TemplateNotFound
from ailerons_tracker_backend.models.article_model import Article
from ailerons_tracker_backend.errors import CloudinaryError, InvalidFile
from ailerons_tracker_backend.upload_image import upload_image


news = Blueprint('news', __name__,
                 template_folder='templates')


@news.get('/news')
@flask_login.login_required
def show():
    """ Serve portal homepage """
    try:
        # Render template returns raw HTML
        return render_template('base_layout.jinja', route="news")

    except TemplateNotFound:
        abort(404)


@news.post('/news')
@flask_login.login_required
def upload_article():
    """ Parse form data and insert news article in DB """
    try:
        image_url = upload_image(request.files['newsImage'])
        article_data = Article(request.form, image_url).upload()
        return article_data, 200

    except (InvalidFile, CloudinaryError) as e:
        current_app.logger.error(e.message)
        return e.message, 400

    except postgrest.exceptions.APIError as e:
        current_app.logger.error(e.message)
        return e.message, 304
