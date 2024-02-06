""" Server and routes """
import sys
import os
from flask import request, current_app
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from ailerons_tracker_backend.clients.cloudinary_client import upload_image
from ailerons_tracker_backend.csv_parser import csv_parser

from ailerons_tracker_backend.models.article_model import Article

from .clients.supabase_client import supabase
from .errors import InvalidFileName

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

app = current_app


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
            content = e.__dict__.get("message")
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
        return e.__dict__.get("message"), 400
