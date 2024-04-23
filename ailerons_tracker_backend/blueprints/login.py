""" Login blueprint """

from ailerons_tracker_backend.models.user_model import User
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
    provided_pwd = request.form["password"]

    if User.check_pwd(provided_pwd):
        flask_login.login_user(User())
        return redirect(url_for('portal.dashboard.show')), 200

    return render_partial('login/login_section.jinja', error_message=True)


@login.get('/')
def show():
    """ Retrieve the login section HTML template """

    htmx = HTMX(current_app)
    try:
        if htmx:
            return make_response(
                render_partial('login/login_section.jinja'),
                replace_url='/portal/login'), 200

        return render_template('base_layout.jinja', view='login'), 200

    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)
