""" GeoJSON Features Models """
import logging
from geojson import Feature, Point, LineString
from .feature_properties import PointProperties, LineProperties


class PointFeature:
    """ Model for Point entry """

    def __init__(self, record, individual):
        self.record_id = record["id"]
        self.csv_id = record["csv_id"]
        self.individual_id = individual["id"]
        self.geojson = self.__to_point_feature(record, individual)

    @staticmethod
    def __to_point_feature(record, individual):
        """ Create a Point GeoJSON Feature """

        props = PointProperties(record, individual)
        geojson = Feature(geometry=Point(
            (record["longitude"], record["latitude"])), properties=props.__dict__)

        if geojson.is_valid:
            return geojson

        logging.error("invalid geoJSON")


class LineStringFeature:
    """ Model for Linestring entry """

    def __init__(self, records, individual):
        self.record_ids = map(lambda record: record["id"], records)
        self.csv_ids = map(lambda record: record["csv_id"], records)
        self.individual_id = individual["id"]
        self.geojson = self.__to_line_feature(records, individual)

    @staticmethod
    def __to_line_feature(ind_records, individual):
        """ Create a LineString GeoJSON Feature """
        props = LineProperties(ind_records, individual)
        coordinates = list(
            map(lambda record: (record["longitude"], record["latitude"]), ind_records))
        geojson = Feature(geometry=LineString(
            coordinates), properties=props.__dict__)

        if geojson.is_valid:
            return geojson