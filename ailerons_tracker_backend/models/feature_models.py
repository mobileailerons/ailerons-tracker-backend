""" GeoJSON Features Models """

import logging
from geojson import Feature, Point, LineString
from sqlalchemy import JSON, ForeignKey, Integer
from sqlalchemy.orm import Mapped
from ailerons_tracker_backend.geojson_generator.data_classes.feature_properties import PointProperties, LineProperties
from ailerons_tracker_backend.db import db
from sqlalchemy.orm import mapped_column as mc, relationship as rel


class PointFeature(db.Model):
    """ Model for Point entry """
    id: Mapped[int] = mc(Integer, primary_key=True, unique=True)
    record_id: Mapped[int] = mc(Integer, ForeignKey('record.id'))
    record: Mapped['record'] = rel(back_populates='record', cascade='all')
    individual_id: Mapped[int] = mc(Integer, ForeignKey('individual.id'))
    individual: Mapped['ind'] = rel(back_populates='individual', cascade='all')
    geojson: Mapped[Point] = mc(JSON)


def __to_point_feature(record, individual):
    """ Create a Point GeoJSON Feature """

    props = PointProperties(record, individual)
    geojson = Feature(geometry=Point(
        (record["longitude"], record["latitude"])), properties=props.__dict__)

    if geojson.is_valid:
        return geojson

    logging.error("invalid geoJSON")


class LineStringFeature(db.Model):
    """ Model for Linestring entry """
    id: Mapped[int] = mc(Integer, primary_key=True, unique=True)
    record_id: Mapped[int] = mc(Integer, ForeignKey('record.id'))
    record: Mapped['record'] = rel(back_populates='record', cascade='all')
    individual_id: Mapped[int] = mc(Integer, ForeignKey('individual.id'))
    individual: Mapped['ind'] = rel(back_populates='individual', cascade='all')
    geojson: Mapped[LineString] = mc(JSON)


def __to_line_feature(ind_records, individual):
    """ Create a LineString GeoJSON Feature """

    props = LineProperties(ind_records, individual)
    coordinates = list(
        map(lambda record: (record["longitude"], record["latitude"]), ind_records))
    geojson = Feature(geometry=LineString(
        coordinates), properties=props.__dict__)

    if geojson.is_valid:
        return geojson
