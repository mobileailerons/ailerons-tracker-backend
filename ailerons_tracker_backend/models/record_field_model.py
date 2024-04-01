""" Record Field Model """

from datetime import datetime

class RecordField:
    """ Model for a field of data record. """

    @staticmethod
    def date_to_iso(excel_date_string):
        """ Parses an excel D/M/Y H:M date string and returns an ISO formatted datestring. """

        return datetime.strptime(excel_date_string, "%d/%m/%Y %H:%M").isoformat()

    def __init__(self, field_name: str, row):
        self.field_name = field_name
        self.field_value = row[field_name]
        self.record_timestamp = self.date_to_iso(row['record_timestamp'])