"""File Manager"""

import os
from pathlib import Path
from werkzeug.utils import secure_filename

from ailerons_tracker_backend.errors import InvalidFile
from ailerons_tracker_backend.models.file_model import File
from ..clients.supabase_client import supabase

class FileManager:
    def __init__(self):
        self.files = []
    
    def prepare_csv_file(self, request, file_tag: str):
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
        
    def drop_all(self):
        """Delete all the files contained in the file manager"""
        for file in enumerate(self.files):
            os.remove(file.path)