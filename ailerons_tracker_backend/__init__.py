""" Configuration and factory for the app """

__version__ = "0.6"

import os
from pathlib import Path
from flask import Flask, request
import postgrest
from werkzeug.utils import secure_filename
from ailerons_tracker_backend.models.article_model import Article
from ailerons_tracker_backend.models.ind_model import Individual, Context
from ailerons_tracker_backend.csv_parser import csv_parser
from ailerons_tracker_backend.geojson_generator.generator import Generator
from .upload_image import upload_image
from .errors import CloudinaryError, GeneratorError, ImageNameError, InvalidFile, SupabaseError
from .clients.supabase_client import supabase


def create_app(test_config=None):
    """ Create an instance of the app """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.post('/upload')
    def upload_file():
        """ Parse a CSV file and insert data in DB

        Returns:
            201: Successful operation
            e: Error while attempting insert in DB """

        try:
            # A priori on aurait deux fichiers donc j'ai donné un nouveau nom à celui ci "
            file_name, file_path = csv_parser.prepare_csv(request)

            csv_id = supabase.create_csv_log(file_name)

            # plus besoin de la table jointe si j'ai bien compris mais je n'y ai pas touché
            df_list, new_individual_id_list = csv_parser.parse_csv(
                file_path, csv_id)

            supabase.batch_insert("record", df_list)
            supabase.batch_insert("individual_record_id",
                                  new_individual_id_list)

            os.remove(file_path)

            generator = Generator()

            generator.generate()
            generator.upload_files()

            content = {"message": "CSVs uploaded and geoJSON generated",
                       "CSV ID": csv_id}

            return content, 200

        # Erreur supabase
        except postgrest.exceptions.APIError as e:
            app.logger.error(e.message)
            return SupabaseError(e), 304

        except GeneratorError as e:
            app.logger.error(e.message)
            app.logger.error(e.base_error)
            return e, 500

        except SupabaseError as e:
            app.logger.error(e.message)
            app.logger.error(e.base_error)
            return e, 204

        except InvalidFile as e:
            app.logger.error(e.message)
            return e, 400

    @app.post('/news')
    def upload_article():
        """ Parse form data and insert news article in DB.

        Raises:
            CloudinaryError: something went wrong when uploading the image file.

        Returns:
            data, 201: Newly created row data, document successfully created.
            error, 400: Error while attempting insert, bad request. """

        try:
            image = request.files['newsImage']
            image_url = upload_image(image)

            new_article = Article(request.form, image_url)
            article_data = new_article.upload()

            return article_data, 200

        except InvalidFile as e:
            app.logger.error(e.message)
            return e.message, 400

        except CloudinaryError:
            app.logger.error(e.message)
            return e.message, 400

        except postgrest.exceptions.APIError as e:
            app.logger.error(e.message)
            return e.message, 304

        except ImageNameError as e:
            app.logger.error(e)
            return e.message, 400

    @app.post('/individual')
    def create_individual():
        try:
            items = request.files.items(multi=True)
            image_urls = []

            for item in items:
                image = item[1]

                image_url = upload_image(image)

                image_urls.append(image_url)

            app.logger.critical(request.form)
            new_ind = Individual(request.form, image_urls)
            ind_data = new_ind.upload()
            ind_id = ind_data.__dict__.get('id')

            new_context = Context(ind_id, request.form)
            context_data = new_context.upload()

            content = {
                'message': 'Successfully uploaded new individual',
                'Individual data': ind_data.__dict__,
                'Context': context_data.__dict__
            }

            return content, 201

        except postgrest.exceptions.APIError as e:
            app.logger.error(e.message)
            return e.message, 304

        except InvalidFile as e:
            app.logger.error(e.message)
            return e.message, 400

        except ImageNameError as e:
            app.logger.error(e.message)
            return e.message, 400

    return app
