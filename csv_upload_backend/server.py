""" Server and routes """
import sys
import os
from flask import Flask, request
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd
from werkzeug.utils import secure_filename
from .record_model import Record
from .article_model import Article
from .cloudinary_client import upload_image

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(supabase_url, supabase_key)

def get_individual_id_list():
    """ Get all individual_ids from join table """
    data = supabase.table('individual_record_id').select("*").execute()

    individual_id_list = []

    for individual in data[1]:
        individual_id_list.append({'individual_id': individual['individual_id']})

    return individual_id_list


def parse_csv(path, csv_id: str):
    """ Parse a CSV file and return a list of entries 
        and a list of matching individual_ids """
    absolute_path = os.path.abspath(path)
    df = pd.read_csv(
        absolute_path,
        index_col=None,
        encoding='ISO-8859-1',
        engine='python',
        on_bad_lines='error',
        sep=';')

    df_list = []
    individual_id_list = get_individual_id_list()
    new_individual_id_list = []

    for row in df.itertuples(index=False):

        if not any(entry['individual_id'] == row.individual_id for entry in individual_id_list):
            individual_id_list.append({ 'individual_id': row.individual_id })
            new_individual_id_list.append({ 'individual_id': row.individual_id })

        new_record = Record(row._asdict())
        new_record.csv_id = csv_id
        df_list.append(new_record.__dict__)

    return df_list, new_individual_id_list

def create_csv_log(file_name: str):
    """ Inserts the CSV file name in the DB and returns the generated ID """
    csv_log = {'file_name': file_name}
    data = supabase.table('csv').insert(csv_log).execute()

    return data[1][0]['id']

app = Flask(__name__)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """ 
    
    Parse a CSV file and insert data in DB

    Returns:
        204: Successful operation
        e: Error while attempting insert in DB
        
    """
    if request.method == 'POST':
        try:
            file = request.files['csvFile']
            if file.filename == '':
                return "No selected file"

            file_name = secure_filename(file.filename)
            # file_path = os.path.join('/usr/src/app/uploaded_csv', file_name)
            file_path = os.path.join('./uploaded_csv', file_name)
            file.save(file_path)

            csv_id = create_csv_log(file_name)

            df_list, new_individual_id_list = parse_csv(file_path, csv_id)

            try:
                supabase.table('record').insert(df_list).execute()
                supabase.table('individual_record_id').insert(new_individual_id_list).execute()
            except Exception as e:
                return e.__dict__["message"], 400

            os.remove(file_path)

            return 204

        except Exception as e:
            return f"Error: {e}"

@app.route('/news', methods=['GET','POST'])
def upload_article():
    """ Parse formdata and insert news article in DB.

    Raises:
        CloudinaryError: something went wrong when uploading the image file.

    Returns:
        data, 201: Newly created row data, document successfully created.
        error, 400: Error while attempting insert, bad request.
    """
    if request.method == 'POST':
        try:
            image = request.files['newsImage']

            if image.filename == '':
                return "No selected file"

            image_name = secure_filename(image.filename)
            image_path = os.path.join('./uploaded_img', image_name)
            image.save(image_path)

            if os.path.exists(image_path):
                image_url = upload_image(image_name, image_path)

            if image_url:
                os.remove(image_path)

        except Exception as error:
            return error.__dict__, 400

        article_data = {
            'title': request.form['newsTitle'],
            'content': request.form['newsContent'],
            'image_url': image_url,
            'published': False,
            'archived': False,
            'publication_date': request.form['newsDate']
        }

        new_article = Article(article_data)

        try:
            data = supabase.table('article').upsert(new_article.__dict__).execute()


        except Exception as e:
            content = e.__dict__["message"], 400
            return content, 400

        content = data.__dict__
        return content, 201
