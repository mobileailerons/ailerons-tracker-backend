""" Record Model """

from datetime import datetime

class Record:
    """ Model for a GPS data record. """

    @staticmethod
    def date_to_iso(excel_date_string):
        """ Parses an excel D/M/Y H:M date string and returns an ISO formatted datestring. """

        return datetime.strptime(excel_date_string, "%d/%m/%Y %H:%M").isoformat()

    def __init__(self, localisation_field_record, depth_field_record):
        self.latitude = localisation_field_record['latitude']
        self.longitude = localisation_field_record['longitude']
        self.depth = depth_field_record['depth']
        self.record_id = localisation_field_record['db_id']
        self.record_timestamp = localisation_field_record['record_timestamp']
