""" Portal blueprint """
from flask import Blueprint, abort, current_app, render_template
from jinja2 import TemplateNotFound
from ailerons_tracker_backend.blueprints.csv_upload import csv_upload
from ailerons_tracker_backend.blueprints.individual_infos import individual_infos
from ailerons_tracker_backend.blueprints.news import news
from ailerons_tracker_backend.clients.supabase_client import supabase
from ailerons_tracker_backend.blueprints.dashboard import dashboard


portal = Blueprint('portal', __name__,
                   template_folder='templates', static_folder='static', url_prefix='/portal')

portal.register_blueprint(csv_upload)
portal.register_blueprint(news)
portal.register_blueprint(individual_infos)
portal.register_blueprint(dashboard)

@portal.route('/')
def show():
    """ Serve csv upload page """
    try:
        inds = supabase.get_all("individual_new")

        # Render template returns raw HTML
        return render_template('base_layout.jinja', inds=inds)

    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)
