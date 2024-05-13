""" Portal blueprint """

from flask import Blueprint, abort, current_app, render_template
from jinja2 import TemplateNotFound
from ailerons_tracker_backend.blueprints.dashboard import dashboard
from ailerons_tracker_backend.blueprints.csv_upload import csv_upload
from ailerons_tracker_backend.blueprints.login import login

portal = Blueprint('portal', __name__,
                   template_folder='templates',
                   static_folder='static',
                   url_prefix='/portal')

portal.register_blueprint(dashboard)
portal.register_blueprint(csv_upload)
portal.register_blueprint(login)


@portal.route('/')
def show():
    """ Serve portal """

    try:
        # Render template returns raw HTML
        return render_template('base_layout.jinja', view='dashboard')

    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)
