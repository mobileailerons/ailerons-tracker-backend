import flask_login
from jinja_partials import render_partial
from flask import Blueprint, render_template, abort, current_app
from jinja2 import TemplateNotFound
from ailerons_tracker_backend.clients.supabase_client import supabase

dashboard = Blueprint('dashboard', __name__, template_folder='templates')

@dashboard.get('/dashboard')
@flask_login.login_required
def show():
    """ Get dashboard window """
    try:
        current_app.logger.warning(flask_login.current_user.is_authenticated)
        individuals = supabase.get_all('individual_new')
        return render_template('dashboard/dashboard.jinja', inds=individuals)
    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)

@dashboard.get('/individuals')
@flask_login.login_required
def show_individuals():
    """ Get dashboard window 'individuals' view """
    try:
        individuals = supabase.get_all('individual_new')
        return render_partial('dashboard/individual_table.jinja', inds=individuals)
    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)

@dashboard.get('/csvs')
@flask_login.login_required
def show_files():
    """ Get dashboard window 'files' view """
    try:
        csvs = supabase.get_all('csv')
        return render_partial('dashboard/csv_table.jinja', csvs=csvs)
    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)
