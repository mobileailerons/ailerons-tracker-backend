""" Portal blueprint """

from flask import Blueprint, abort, current_app, render_template
from jinja2 import TemplateNotFound
from ailerons_tracker_backend.blueprints.dashboard import dashboard

portal = Blueprint('portal', __name__,
                   template_folder='templates', static_folder='static', url_prefix='/portal')

portal.register_blueprint(dashboard)


@portal.route('/')
def show():
    """ Serve portal """
    try:
        # Render template returns raw HTML
        return render_template('base_layout.jinja')

    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)
