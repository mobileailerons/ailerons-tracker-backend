""" CSV file parser middleware """
from ailerons_tracker_backend.errors import ParserError
from ailerons_tracker_backend.models.record_model import Record
from ailerons_tracker_backend.models.record_field_model import RecordField
from ailerons_tracker_backend.models.file_model import File
from ailerons_tracker_backend.utils.file_util import FileManager

class CsvParser:
    """Class that manage the parsing of the different csv"""
    def __init__(self, loc_file, depth_file):
        self.loc_df = self._parse_field_from_csv(loc_file, "localisation")
        self.depth_df = self._parse_field_from_csv(depth_file, "profondeur")
        self.record_df = "TODO"

    def _parse_field_from_csv(self, file: File, field_name):
        try:
            file_df = FileManager().get_dataframe(file.path)
            data_list = []

            for row in file_df.itertuples(index=False):
                new_field_record = RecordField(field_name, row._asdict())
                new_field_record.file_db_id = file.db_id
                data_list.append(new_field_record.__dict__)

            return data_list
        except Exception as e:
            raise ParserError() from e
