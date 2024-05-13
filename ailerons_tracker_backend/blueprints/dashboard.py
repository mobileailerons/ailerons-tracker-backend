""" Dashboard blueprint """

from flask_htmx import HTMX
from jinja_partials import render_partial
from flask import Blueprint, abort, current_app, render_template
from flask_login import login_required
from jinja2 import TemplateNotFound

from ailerons_tracker_backend.db import db
from ailerons_tracker_backend.models.individual_model import Individual

dashboard = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard.get('/dashboard')
@login_required
def show():
    """ Get dashboard window """

    htmx = HTMX(current_app)

    try:
        individuals = db.session.execute(
            db.select(Individual)
        ).scalars().all()


        if htmx:

            return render_partial('dashboard/dashboard.jinja', inds=individuals)

        return render_template('base_layout.jinja', view='dashboard')

    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)
