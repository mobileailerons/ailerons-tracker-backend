""" Upload CSV files blueprint """

from pathlib import Path
import postgrest
from werkzeug.utils import secure_filename
from ailerons_tracker_backend.models.individual_model import Individual
from ailerons_tracker_backend.models.csv_model import Csv
from flask_login import login_required
from pandas import Timedelta, pandas as pd
from ailerons_tracker_backend.db import db
from ailerons_tracker_backend.geojson_generator.generator import generate
from ailerons_tracker_backend.errors import GeneratorError, MissingParamError
from ailerons_tracker_backend.clients.supabase_client import supabase
from jinja2 import TemplateNotFound
from flask import Blueprint, abort, render_template, request, current_app
from jinja_partials import render_partial
from flask_htmx import HTMX

csv = Blueprint('csv', __name__,
                template_folder='templates', url_prefix="csv")


@csv.post('/upload')
@login_required
def upload_file():
    """ Parse a CSV file and insert data in DB """
    try:
        ind_id = request.args.get("id", type=int)

        loc_file = request.files['loc_file']
        depth_file = request.files['depth_file']

        individual = db.session.get_one(Individual, ind_id)
        individual.csv = Csv(
            loc_file=secure_filename(
                Path(loc_file.filename).stem
            ),
            depth_file=secure_filename(Path(depth_file.filename).stem))

        db.session.commit()

        loc_df = pd.read_csv(
            loc_file,
            header=4,
            sep=',',
            decimal='.',
            index_col=None,
            encoding='ISO-8859-1',
            engine='python',
            on_bad_lines='error')

        loc_df['record_timestamp'] = loc_df['Date'].apply(
            pd.to_datetime)

        loc_df = loc_df.filter(
            ['Most Likely Latitude', 'Most Likely Longitude', 'record_timestamp',])
        loc_df = loc_df.rename(columns={'Most Likely Latitude': 'latitude',
                                        'Most Likely Longitude': 'longitude'})

        loc_df = loc_df.sort_values(by="record_timestamp")

        depth_df = pd.read_csv(
            depth_file,
            header=0,
            sep=',',
            decimal='.',
            index_col=None,
            encoding='ISO-8859-1',
            engine='python',
            on_bad_lines='error')

        depth_df['record_timestamp'] = depth_df['Day'] + \
            " " + depth_df['Time']

        depth_df['record_timestamp'] = depth_df['record_timestamp'].apply(
            pd.to_datetime)

        depth_df = depth_df.filter(['record_timestamp', 'Depth'])
        depth_df = depth_df.rename(columns={'Depth': 'depth'})

        depth_df = depth_df.sort_values(by="record_timestamp")

        t_delta = Timedelta(100, unit='min')

        df = pd.merge_asof(
            loc_df, depth_df, on='record_timestamp', tolerance=t_delta)

        df = df.assign(csv_uuid=individual.csv.uuid,
                       individual_id=individual.id)

        df.to_sql(name='record', con=db.engine,
                  if_exists='append', index=False)

        db.session.commit()

        generate(individual, db)

        return render_partial('dashboard/dashboard.jinja'), 200

    except GeneratorError as e:
        current_app.logger.error(e.message)
        return e.message, 500

    except postgrest.exceptions.APIError as e:
        current_app.logger.error(e.message)
        return e.message, 304


@csv.get('/upload')
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
