from flask import Flask
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import pandas as pd
from record_model import Record

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

def parse_csv(path):
    
    absolute_path = os.path.abspath(path)
    df = pd.read_csv(absolute_path, index_col=None, encoding='ISO-8859-1', engine='python', on_bad_lines='error', sep=';')

    df_list = []
    for row in df.itertuples(index=False):
        new_record = Record(row._asdict())
        new_record.csv_id = 1 # for test purpose
        df_list.append(new_record.__dict__)

    data, count = supabase.table('record').insert(df_list).execute()
    print(data, count)

    return df
    
parse_csv("./data_test.csv")

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"