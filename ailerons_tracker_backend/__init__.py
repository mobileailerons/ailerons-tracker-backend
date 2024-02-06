""" Configuration and factory for the app """

__version__ = "0.5"

import os
from flask import Flask, request
from werkzeug.utils import secure_filename
from ailerons_tracker_backend.models.article_model import Article
from ailerons_tracker_backend.clients.cloudinary_client import upload_image
from ailerons_tracker_backend.errors import InvalidFileName
from ailerons_tracker_backend.csv_parser import csv_parser
from .clients.supabase_client import supabase
from .errors import InvalidFileName


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

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        """ Parse a CSV file and insert data in DB

        Returns:
            204: Successful operation
            e: Error while attempting insert in DB """

        if request.method == 'POST':
            try:
                file = request.files['csvFile']

                if file.filename == '':
                    raise InvalidFileName()

                file_name = secure_filename(file.filename)
                file_path = os.path.join('./uploaded_csv', file_name)
                file.save(file_path)

                csv_id = supabase.create_csv_log(file_name)
                df_list, new_individual_id_list = csv_parser.parse_csv(
                    file_path, csv_id)
                supabase.batch_insert("record", df_list)
                supabase.batch_insert("individual_record_id",
                                      new_individual_id_list)

                os.remove(file_path)
                content = "Successfully uploaded CSV"
                return content, 204

            except Exception as e:
                content = e.__dict__
                return content, 400

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

            if image.filename == '':
                raise InvalidFileName()

            image_name = secure_filename(image.filename)
            image_path = os.path.join('./uploaded_img', image_name)
            image.save(image_path)

            if os.path.exists(image_path):
                image_url = upload_image(image_name, image_path)

            if image_url:
                os.remove(image_path)

            new_article = Article(request.form, image_url)
            data = supabase.upsert_article(new_article)
            return data, 201

        except Exception as e:
            return e.__dict__
        
    return app

    # a simple page that says hello
