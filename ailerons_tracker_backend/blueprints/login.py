""" Login blueprint """
import flask_login
from dotenv import load_dotenv
from flask import current_app, Blueprint, abort, redirect, request, url_for
from jinja2 import TemplateNotFound
from jinja_partials import render_partial

from ailerons_tracker_backend.models.user_model import User

load_dotenv()

login = Blueprint('login', __name__,
                  template_folder='templates', url_prefix='login')


@login.post('/')
def connect():
    """ Connect to the app """
    provided_pwd = request.form["password"]

    if User.check_pwd(provided_pwd):
        flask_login.login_user(User())

        return redirect(url_for('portal.dashboard.show'))

    return render_partial('login/login_section.jinja', error_message=True)


@login.get('/')
def show():
    """ Retrieve the login section HTML template """
    try:
        return render_partial('login/login_section.jinja')

    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)
