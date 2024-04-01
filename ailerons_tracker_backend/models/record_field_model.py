""" Record Field Model """

from datetime import datetime

class Record:
    """ Model for a field of data record. """

    @staticmethod
    def date_to_iso(excel_date_string):
        """ Parses an excel D/M/Y H:M date string and returns an ISO formatted datestring. """

        return datetime.strptime(excel_date_string, "%d/%m/%Y %H:%M").isoformat()

    def __init__(self, field_name: str, field_value, field_timestamp):
        self.field_name = field_name
        self.field_value = field_value
        self.field_timestamp = self.date_to_iso(field_timestamp)