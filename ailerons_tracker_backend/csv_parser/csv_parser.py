""" CSV file parser middleware """
import os
from pathlib import Path
import pandas as pd
from werkzeug.utils import secure_filename

from ailerons_tracker_backend.errors import InvalidFile, ParserError
from ailerons_tracker_backend.models.record_model import Record
from ailerons_tracker_backend.models.file_model import File
from ..clients.supabase_client import supabase

class CsvParser:
    def __init__(self, request):
        self.loc_file = File(self._prepare_csv_file(request, "locFile"))
        self.depth_file = File(self._prepare_csv_file(request, "depthFile"))

    def _prepare_csv_file(self, request, file_tag: str):
        try:
            file = request.files[file_tag]
            stem = Path(file.filename).stem

            file_name = secure_filename(stem)

            file_path = os.path.join('./uploaded_csv', file_name)
            file.save(file_path)
            file_db_id: int = supabase.create_csv_log(file_name)

            return file_path, file_db_id
        
        except Exception as e:
            raise InvalidFile(e) from e


def parse_csv(path, csv_id: str, field_to_parse: str):
    """ Parse a CSV file and return a list of entries 
        and a list of matching individual_ids """
    try:
        absolute_path = os.path.abspath(path)
        record_df = pd.read_csv(
            absolute_path,
            index_col=None,
            encoding='ISO-8859-1',
            engine='python',
            on_bad_lines='error',
            sep=';')

        df_list = []

        for row in record_df.itertuples(index=False):
            new_record = Record(row._asdict())
            new_record.csv_id = csv_id
            record_list.append(new_record.__dict__)

        return df_list

    except Exception as e:
        raise ParserError() from e
