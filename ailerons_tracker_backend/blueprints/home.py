""" Portal homepage blueprint """
from flask import Blueprint, render_template, abort

from jinja2 import TemplateNotFound


home = Blueprint('home', __name__,
                 template_folder='templates', static_folder='static')


@home.route('/home')
def show():
    """ Serve portal homepage """
    try:
        # Render template returns raw HTML
        return render_template('home.html')

    except TemplateNotFound:
        abort(404)