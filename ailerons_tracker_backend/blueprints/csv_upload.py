""" Upload CSV files blueprint """

import uuid
import postgrest
from flask_htmx import HTMX, make_response
from jinja_partials import render_partial
from flask import Blueprint, abort, render_template, request, current_app
from jinja2 import TemplateNotFound
from ailerons_tracker_backend.clients.supabase_client import supabase
from ailerons_tracker_backend.csv_parser.csv_parser import CsvParser
from ailerons_tracker_backend.errors import GeneratorError, InvalidFile, MissingParamError
from ailerons_tracker_backend.utils.file_util import FileManager
from flask_login import login_required

csv_upload = Blueprint('csv_upload', __name__,
                       template_folder='templates', url_prefix="csv")


@csv_upload.post('/upload')
@login_required
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

        return make_response(render_partial('dashboard/dashboard.jinja'), push_url='/dashboard'), 200

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


@csv_upload.get('/upload')
@login_required
def show():
    """ Serve csv upload page """
    try:
        htmx = HTMX(current_app)

        individual_id = request.args.get('id')

        if not individual_id:
            raise MissingParamError('id')

        individual_data = supabase.get_exact(
            'id', individual_id, "individual")

        if htmx:
            return render_partial('csv_upload/csv_upload.jinja',
                                  ind=individual_data)

        return render_template('base_layout.jinja', view=f'upload?id={individual_id}')

    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)

    except MissingParamError as e:
        current_app.logger.error(e)
        return e, 400
