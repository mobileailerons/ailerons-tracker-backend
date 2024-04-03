"""File Manager"""

import os
from pathlib import Path
from enum import Enum
import pandas as pd
from werkzeug.utils import secure_filename
import postgrest

from ailerons_tracker_backend.errors import InvalidFile


class FileFieldName(Enum):
    """Enum class that indicate the field that should be parsed in the file"""
    LOCALISATION = "loc"
    DEPTH = "depth"


class File:
    """ Model for a CSV file. """

    def __init__(self, file_path, file_field_name, csv_uuid):
        self.path = file_path
        self.field_name = file_field_name
        self.csv_uuid = csv_uuid


class FileManager:
    """File Manager"""

    def __init__(self, request, csv_uuid: str):
        self.files = []
        self.request = request
        self.csv_uuid = csv_uuid
        

    def prepare_csv_file(self, file_field_name: FileFieldName):
        """Get the file with the corresponding file tag in the request and move it in a folder.
        Create a file id in the database and return this id and the file path"""
        try:
            file_tag = f"{file_field_name.value}_file"
            file = self.request.files[file_tag]
            stem = Path(file.filename).stem

            file_name = secure_filename(stem)
            file_path = os.path.join('./uploaded_csv', file_name)
            file.save(file_path)

            file = File(file_path, file_field_name, self.csv_uuid)
            self.files.append(file)
            return file

        except postgrest.exceptions.APIError as e:
            print(e.message)
            raise e

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
        for file in self.files:
            os.remove(file.path)
