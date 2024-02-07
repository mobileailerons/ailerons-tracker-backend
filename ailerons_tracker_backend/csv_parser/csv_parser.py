""" CSV file parser middleware """
import os
import pandas as pd

from ailerons_tracker_backend.clients.supabase_client import supabase
from ailerons_tracker_backend.models.record_model import Record


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
    individual_id_list = supabase.get_individual_ids()
    new_individual_id_list = []

    for row in df.itertuples(index=False):

        if not any(entry['individual_id'] == row.individual_id for entry in individual_id_list):
            individual_id_list.append({'individual_id': row.individual_id})
            new_individual_id_list.append({'individual_id': row.individual_id})

        new_record = Record(row._asdict())
        new_record.csv_id = csv_id
        df_list.append(new_record.__dict__)

    return df_list, new_individual_id_list
