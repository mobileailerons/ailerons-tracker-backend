""" Dashboard blueprint """

from flask_htmx import HTMX, make_response
from jinja_partials import render_partial
from flask import Blueprint, render_template, abort, current_app
from flask_login import login_required
from jinja2 import TemplateNotFound
from ailerons_tracker_backend.clients.supabase_client import supabase

dashboard = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard.get('/dashboard')
@login_required
def show():
    """ Get dashboard window """
    htmx = HTMX(current_app)

    try:
        individuals = supabase.get_all('individual')

        if htmx:
            return make_response(
                render_partial('dashboard/dashboard.jinja', inds=individuals),
            replace_url='/portal/dashboard')

        return render_template('base_layout.jinja', view="dashboard")

    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)
