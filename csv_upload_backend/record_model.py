""" Record Model """

from datetime import datetime

class Record:
    """ Model for a GPS data record. """

    @staticmethod
    def date_to_iso(excel_date_string):
        """ Parses an excel D/M/Y H:M date string and returns an ISO formatted datestring. """

        return datetime.strptime(excel_date_string, "%d/%m/%Y %H:%M").isoformat()

    def __init__(self, row):
        self.latitude = row['latitude'].replace(',', '.')
        self.longitude = row['longitude'].replace(',', '.')
        self.individual_id = row['individual_id']
        self.record_timestamp = self.date_to_iso(row['record_timestamp'])
        