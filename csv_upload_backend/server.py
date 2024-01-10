from flask import Flask, request
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import pandas as pd
from record_model import Record
from werkzeug.utils import secure_filename

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

def parse_csv(path, csv_id):
    absolute_path = os.path.abspath(path)
    df = pd.read_csv(absolute_path, index_col=None, encoding='ISO-8859-1', engine='python', on_bad_lines='error', sep=';')

    df_list = []
    for row in df.itertuples(index=False):
        new_record = Record(row._asdict())
        new_record.csv_id = csv_id
        df_list.append(new_record.__dict__)

    return df_list

def create_csv_log(file_name):
    csv_log = {'file_name': file_name }
    data, count = supabase.table('csv').insert(csv_log).execute()
    return data[1][0]['id']

app = Flask(__name__)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
            file = request.files['csvFile']
            if file.filename == '':
                return "No selected file"

            file_name = secure_filename(file.filename)
            file_path = os.path.join('./uploaded_csv', file_name)
            file.save(file_path)

            csv_id = create_csv_log(file_name)

            data, count = supabase.table('record').insert(parse_csv(file_path, csv_id)).execute()
            print(data, count)

            return "Fichiers envoyés avec succès"

        except Exception as e:
            return f"Error: {e}"

    
