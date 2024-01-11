from flask import Flask, request
from supabase import create_client, Client
from dotenv import load_dotenv
import sys
import os
import pandas as pd
from .record_model import Record
from werkzeug.utils import secure_filename

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

# supabase_url = os.getenv("SUPABASE_URL")
# supabase_key = os.getenv("SUPABASE_KEY")
supabase_url='https://rddizwstjdinzyzvnuun.supabase.co'
supabase_key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJkZGl6d3N0amRpbnp5enZudXVuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwNDg5NTcwMywiZXhwIjoyMDIwNDcxNzAzfQ.cc143ySM1DZgtb1ADUP7p_HRdIpbaLp3X4ICf94rZD4'

supabase: Client = create_client(supabase_url, supabase_key)

def get_individual_id_list():
    data, count = supabase.table('individual_record_id').select("*").execute()

    individual_id_list = []

    for individual in data[1]:
        individual_id_list.append({'individual_id': individual['individual_id']})

    return individual_id_list


def parse_csv(path, csv_id):
    absolute_path = os.path.abspath(path)
    df = pd.read_csv(absolute_path, index_col=None, encoding='ISO-8859-1', engine='python', on_bad_lines='error', sep=';')

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
            file_path = os.path.join('/usr/src/app/uploaded_csv', file_name)
            print("hey")
            file.save(file_path)
            print("oi")

            csv_id = create_csv_log(file_name)

            df_list, new_individual_id_list = parse_csv(file_path, csv_id)

            data, count = supabase.table('record').insert(df_list).execute()
            data, count = supabase.table('individual_record_id').insert(new_individual_id_list).execute()

            os.remove(file_path)
            
            return "Fichiers envoyés avec succès"

        except Exception as e:
            return f"Error: {e}"
        

    
