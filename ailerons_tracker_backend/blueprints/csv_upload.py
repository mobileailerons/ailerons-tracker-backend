""" Upload CSV files blueprint """

import uuid
import postgrest
from flask_htmx import HTMX, make_response
from jinja_partials import render_partial
from flask import Blueprint, abort, flash, render_template, request, current_app
from jinja2 import TemplateNotFound
from ailerons_tracker_backend.clients.supabase_client import supabase
from ailerons_tracker_backend.csv_parser.csv_parser import CsvParser
from ailerons_tracker_backend.errors import GeneratorError, InvalidFile
from ailerons_tracker_backend.utils.file_util import FileManager

csv_upload = Blueprint('csv_upload', __name__,
                       template_folder='templates')


@csv_upload.post('/upload')
def upload_file():
    """ Parse a CSV file and insert data in DB """

    try:
        # On récupère le nom/id de l'individu auquel correspondent les fichiers
        associated_individual = request.args.get("id")

        current_app.logger.warning(associated_individual)

        csv_uuid = str(uuid.uuid4())
        file_manager = FileManager(request, csv_uuid)
        csv_parser = CsvParser(file_manager)

        supabase.create_csv_log(
            csv_uuid, file_manager.loc_file.name, file_manager.depth_file.name)

        supabase.batch_insert("record", csv_parser.record_list)

        file_manager.drop_all()

        return make_response(render_partial('dashboard/dashboard.jina'), push_url='/dashboard'), 200

    # Erreur supabase
    except postgrest.exceptions.APIError as e:
        current_app.logger.error(e.message)
        return e.message, 304

    except GeneratorError as e:
        current_app.logger.error(e.message)
        return e.message, 500

    except InvalidFile as e:
        current_app.logger.error(e.message)
        return e.message, 400


@csv_upload.get('/csv_upload')
def show():
    """ Serve csv upload page """
    try:
        htmx = HTMX(current_app)

        individual_id = request.args.get('id')

        individual_data = supabase.get_exact(
            'id', individual_id, "individual")
        # Render template returns raw HTML
        if (htmx):
            return make_response(
                render_partial('csv_upload/csv_upload.jinja',
                               ind=individual_data),
                replace_url=f'/portal/csv_upload?id={individual_id}')

        return render_template('base_layout.jinja')

    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)
