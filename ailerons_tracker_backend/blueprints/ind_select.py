""" Blueprint for the Select HTML element containing a list of all individuals. """

from flask import Blueprint, render_template, abort, current_app
from flask_htmx import HTMX
from jinja2 import TemplateNotFound
from ailerons_tracker_backend.clients.supabase_client import supabase


ind_select = Blueprint('ind_select', __name__,
                       template_folder='templates')


@ind_select.route('/load')
def show():
    """ Generate the list"""
    # This is just to make sure we're receiving an HTMX request
    htmx = HTMX(current_app)
    if htmx:
        try:

            inds = supabase.get_all("individual")
            # Render template returns raw HTML
            return render_template('ind_select.html', inds=inds)
        except TemplateNotFound:
            abort(404)
