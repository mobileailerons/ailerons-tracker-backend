""" Upload CSV files blueprint """

import os
from jinja_partials import render_partial
import postgrest
from flask import Blueprint, abort, request, current_app
from jinja2 import TemplateNotFound
from ailerons_tracker_backend.clients.supabase_client import supabase
from ailerons_tracker_backend.csv_parser import csv_parser
from ailerons_tracker_backend.geojson_generator.generator import Generator
from ailerons_tracker_backend.errors import GeneratorError, InvalidFile


csv_upload = Blueprint('csv_upload', __name__,
                       template_folder='templates')


@csv_upload.post('/upload')
def upload_file():
    """ Parse a CSV file and insert data in DB """

    try:
        # On récupère le nom/id de l'individu auquel correspondent les fichiers
        associated_individual = request.args.get("id")
        current_app.logger.warning(associated_individual)

        # A priori on aurait deux fichiers donc j'ai donné un nouveau nom à celui ci "
        file_name, file_path = csv_parser.prepare_csv(request)
        csv_id = supabase.create_csv_log(file_name)

        # plus besoin de la table jointe si j'ai bien compris mais je n'y ai pas touché
        record_list, new_individual_id_list = csv_parser.parse_csv(
            file_path, csv_id)

        supabase.batch_insert("record", record_list)
        supabase.batch_insert("individual_record_id",
                              new_individual_id_list)

        os.remove(file_path)

        generator = Generator()
        generator.generate()

        return "CSVs uploaded and geoJSONs generated", 200

    # Erreur supabase
    except postgrest.exceptions.APIError as e:
        current_app.logger.error(e.message)
        return e.message, 304

    except GeneratorError as e:
        current_app.logger.error(e.message)
        return e.message, 500

    except InvalidFile as e:
        current_app.logger.error(e)
        return e, 400


@csv_upload.get('/csv')
def show():
    """ Serve csv upload page """
    try:
        individual_id = request.args.get('id')
        individual_data = supabase.get_match('id', individual_id, "individual")[0]
        # Render template returns raw HTML
        return render_partial('csv_upload/csv_upload.jinja', ind=individual_data)

    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)
