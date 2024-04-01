""" Record Field Model """

from datetime import datetime

class RecordField:
    """ Model for a field of data record. """

    @staticmethod
    def date_to_iso(excel_date_string):
        """ Parses an excel D/M/Y H:M date string and returns an ISO formatted datestring. """

        return datetime.strptime(excel_date_string, "%d/%m/%Y %H:%M:%S").isoformat()

    def __init__(self, row: dict):
        self.record_timestamp = self.date_to_iso(row['record_timestamp'])

class DepthField(RecordField):
    """DepthField extends RecordField and contain depth data"""
    def __init__(self, row):
        super().__init__(row)
        self.depth = row['depth']

class LocalisationField(RecordField):
    """LocalisationField extends RecordField and contain localisation data"""
    def __init__(self, row):
        super().__init__(row)
        self.longitude = row['longitude'].replace(',', '.')
        self.latitude = row['latitude'].replace(',', '.')
