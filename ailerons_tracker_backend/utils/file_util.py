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
    LOCALISATION = "loc_file"
    DEPTH = "depth_file"


class File:
    """ Model for a CSV file. """

    def __init__(self, name, file_field_name, df):
        self.name: str = name
        self.field_name: FileFieldName = file_field_name
        self.df = df


class FileManager:
    """File Manager"""

    def __init__(self, request, csv_uuid: str):
        self.files_path: list[str] = []
        self.request = request
        self.csv_uuid = csv_uuid
        self.loc_file: File = self._prepare_csv_file(FileFieldName.LOCALISATION)
        self.depth_file: File = self._prepare_csv_file(FileFieldName.DEPTH)
        

    def _prepare_csv_file(self, file_field_name: FileFieldName):
        """Get the file with the corresponding file tag in the request and move it in a folder.
        Create a file id in the database and return this id and the file path"""
        try:
            file = self.request.files[file_field_name.value]
            stem = Path(file.filename).stem

            file_name = secure_filename(stem)
            file_path = os.path.join('./uploaded_csv', file_name)
            file.save(file_path)
            
            file_df = self._get_dataframe(file_path)
            file = File(file_name, file_field_name, file_df)
            self.files_path.append(file_path)
            return file

        except postgrest.exceptions.APIError as e:
            print(e.message)
            raise e

        except Exception as e:
            raise InvalidFile(e) from e

    def _get_dataframe(self, file_path):
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
        for file_path in self.files_path:
            os.remove(file_path)
