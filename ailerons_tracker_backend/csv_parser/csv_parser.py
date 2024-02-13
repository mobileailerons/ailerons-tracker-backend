""" CSV file parser middleware """
import os
from pathlib import Path
import pandas as pd
from werkzeug.utils import secure_filename

from ailerons_tracker_backend.clients.supabase_client import supabase
from ailerons_tracker_backend.errors import InvalidFile, ParserError
from ailerons_tracker_backend.models.record_model import Record

def prepare_csv(request):
    """ Parse POST request CSV file and make a local copy

    Args:
        request (API request): Request data
    """
    try:
        file = request.files["locFile"]
        stem = Path(file.filename).stem

        file_name = secure_filename(stem)

        file_path = os.path.join('./uploaded_csv', file_name)
        file.save(file_path)
        return file_name, file_path

    except Exception as e:
        raise InvalidFile(e) from e

def parse_csv(path, csv_id: str):
    """ Parse a CSV file and return a list of entries 
        and a list of matching individual_ids """
    try:
        absolute_path = os.path.abspath(path)
        df = pd.read_csv(
            absolute_path,
            index_col=None,
            encoding='ISO-8859-1',
            engine='python',
            on_bad_lines='error',
            sep=';')

        df_list = []
        individual_id_list = supabase.get_individual_ids()
        new_individual_id_list = []

        for row in df.itertuples(index=False):

            if not any(entry['individual_id'] == row.individual_id for entry in individual_id_list):
                individual_id_list.append({'individual_id': row.individual_id})
                new_individual_id_list.append(
                    {'individual_id': row.individual_id})

            new_record = Record(row._asdict())
            new_record.csv_id = csv_id
            df_list.append(new_record.__dict__)

        return df_list, new_individual_id_list

    except Exception as e:
        raise ParserError() from e
