""" Dashboard blueprint """

from flask_htmx import HTMX
from jinja_partials import render_partial
from flask import Blueprint, render_template, abort, current_app
from jinja2 import TemplateNotFound
from ailerons_tracker_backend.clients.supabase_client import supabase

dashboard = Blueprint('dashboard', __name__, template_folder='templates')


@dashboard.get('/dashboard')
def show():
    """ Get dashboard window """
    htmx = HTMX(current_app)

    try:
        individuals = supabase.get_all('individual')

        if htmx:
            return render_partial('dashboard/dashboard.jinja', inds=individuals)

        return render_template('base_layout.jinja')
    
    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)
