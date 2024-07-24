
""" WTForms for individual and context """

from flask_wtf import FlaskForm
from wtforms.fields import FileField


class ContextForm(FlaskForm):
    """ Context form

    Fields:
    """

    loc_file = FileField('Relevés de localisation')
    depth_file = FileField('Relevés de profondeur')
