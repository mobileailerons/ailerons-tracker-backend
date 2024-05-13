""" Login blueprint """

import flask_login
from jinja_partials import render_partial
from jinja2 import TemplateNotFound
from flask import current_app, Blueprint, abort,  render_template
from flask_htmx import HTMX, make_response
from dotenv import load_dotenv
from ailerons_tracker_backend.db import db
from ailerons_tracker_backend.models.individual_model import Individual
from ailerons_tracker_backend.models.user_model import User
from ailerons_tracker_backend.errors import EnvVarError
from ailerons_tracker_backend.forms.login_form import LoginForm

load_dotenv()

login = Blueprint('login', __name__,
                  template_folder='templates', url_prefix='login')


@login.post('/')
def connect():
    """ Connect to the app """

    try:
        form = LoginForm()
        form.validate()
        individuals = db.session.execute(
            db.select(Individual)
        ).scalars().all()

        if User.check_pwd(form.password.data):
            flask_login.login_user(User())

            return make_response(render_partial(
                "dashboard/dashboard.jinja", inds=individuals), push_url="/portal/dashboard")

        return render_partial('login/login_section.jinja',form=form, error_message=True)

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
