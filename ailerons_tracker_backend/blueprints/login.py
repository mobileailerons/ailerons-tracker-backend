""" Login blueprint """

from ailerons_tracker_backend.models.user_model import User
from ailerons_tracker_backend.errors import EnvVarError
from jinja_partials import render_partial
from jinja2 import TemplateNotFound
from flask import current_app, Blueprint, abort, redirect, render_template, request, url_for
from flask_htmx import HTMX, make_response
from dotenv import load_dotenv
import flask_login


load_dotenv()

login = Blueprint('login', __name__,
                  template_folder='templates', url_prefix='login')

@login.post('/')
def connect():
    """ Connect to the app """

    try:
        provided_pwd = request.form["password"]

        if User.check_pwd(provided_pwd):
            flask_login.login_user(User())
            return redirect(url_for('portal.dashboard.show')), 200

        return render_partial('login/login_section.jinja', error_message=True)

    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)

    except EnvVarError as e:
        current_app.logger.warning(e)
        return e, 500


@ login.get('/')
def show():
    """ Retrieve the login section HTML template """

    htmx = HTMX(current_app)
    form = LoginForm()

    try:
        if htmx:
            return render_partial(
                'login/login_section.jinja', form=form)

        return render_template(
            'base_layout.jinja', view='/portal/login', form=form), 200

    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)
