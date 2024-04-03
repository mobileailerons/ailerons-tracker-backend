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

    def __init__(self, file_path, file_field_name):
        self.path: str = file_path
        self.field_name: str = file_field_name


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
            file_tag = f"{file_field_name.value}_file"
            file = self.request.files[file_tag]
            stem = Path(file.filename).stem

            file_name = secure_filename(stem)
            file_path = os.path.join('./uploaded_csv', file_name)
            file.save(file_path)

            file = File(file_path, file_field_name.value)
            self.files_path.append(file.field_name)
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
        for file_path in self.files_path:
            os.remove(file_path)
