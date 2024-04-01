""" Record Model """

from ailerons_tracker_backend.models.record_field_model import LocalisationField, DepthField


class Record:
    """ Model for a GPS data record. """

    def __init__(self, localisation_field_record: LocalisationField, depth_field_record: DepthField):
        self.latitude = localisation_field_record.latitude
        self.longitude = localisation_field_record.longitude
        self.depth = depth_field_record.depth
        self.csv_id = localisation_field_record.csv_id
        self.record_timestamp = localisation_field_record.record_timestamp

    def to_dict(self):
        """Return a dict containing the attributes"""
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "depth": self.depth,
            "csv_id": self.csv_id,
            "record_timestamp": self.record_timestamp
        }
