"""File Manager"""

import os
from pathlib import Path
import pandas as pd
from werkzeug.utils import secure_filename

from ailerons_tracker_backend.errors import InvalidFile
from ailerons_tracker_backend.models.file_model import File
from ..clients.supabase_client import supabase


class FileManager:
    """File Manager"""

    def __init__(self):
        self.files = []

    def prepare_csv_file(self, request, file_tag: str):
        """Get the file with the corresponding file tag in the request and move it in a folder.
        Create a file id in the database and return this id and the file path"""
        try:
            file = request.files[file_tag]
            stem = Path(file.filename).stem

            file_name = secure_filename(stem)

            file_path = os.path.join('./uploaded_csv', file_name)
            file.save(file_path)
            file_db_id: int = supabase.create_csv_log(file_name)

            file = File(file_path, file_db_id)
            self.files.append(file)
            return file

        except Exception as e:
            raise InvalidFile(e) from e
        
    def get_dataframe(self, file_path):
        """Return a dataframe from the file"""
        absolute_path = os.path.abspath(file_path)
        file_df = pd.read_csv(
            absolute_path,
            index_col=None,
            encoding='ISO-8859-1',
            engine='python',
            on_bad_lines='error',
            sep=';')
        return file_df

    def drop_all(self):
        """Delete all the files contained in the file manager"""
        for file in enumerate(self.files):
            os.remove(file.path)
