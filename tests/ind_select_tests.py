""" Ind_select template tests """

from pathlib import Path
from flask import render_template
resources = Path(__file__).parent / "resources"

test_file = (resources / "ind_select_test.jinja").open("r")


def test_ind_select(app):
    """ Test if ind names are rendered. """

    with app.app_context():
        select = render_template('ind_select.jinja', inds=[
                                 {"name": "test"},
                                 {"name": "test2"}])

        assert (
            '<option value="test">test</option>'
            and
            '<option value="test2">test2</option>') in select
