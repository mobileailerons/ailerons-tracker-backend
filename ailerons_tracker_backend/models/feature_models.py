""" GeoJSON Features Models """

from geojson import Feature, Point, LineString
from sqlalchemy import JSON, ForeignKey, Identity, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped
from ailerons_tracker_backend.geojson_generator.data_classes.feature_properties import PointProperties, LineProperties
from ailerons_tracker_backend.db import db
from sqlalchemy.orm import mapped_column as mc, relationship as rel


class PointGeojson(db.Model):
    """ Model for Point entry """
    id: Mapped[int] = mc(postgresql.BIGINT, Identity(
        start=1, always=True), primary_key=True, unique=True)

    created_at: Mapped[str] = mc(
        postgresql.TIMESTAMP(timezone=True), default=func.now())

    record_id: Mapped[int] = mc(postgresql.BIGINT, ForeignKey('record.id'))

    record: Mapped['Record'] = rel(
        back_populates='point_feature')

    individual_id: Mapped[int] = mc(
        postgresql.BIGINT, ForeignKey('individual.id'))

    individual: Mapped['Individual'] = rel(
        back_populates='point_features')

    geojson: Mapped[Point] = mc(JSON)


def to_point_feature(record, individual):
    """ Create a Point GeoJSON Feature """

    props = PointProperties(record, individual)

    geojson = Feature(geometry=Point(
        (record.longitude, record.latitude)), properties=props.__dict__)

    if geojson.is_valid:
        return geojson


class LineGeojson(db.Model):
    """ Model for Linestring entry """

    id: Mapped[int] = mc(postgresql.BIGINT, Identity(
        start=1, always=True), primary_key=True, unique=True)

    individual_id: Mapped[int] = mc(
        postgresql.BIGINT, ForeignKey('individual.id'))

    individual: Mapped['Individual'] = rel(
        back_populates='line_feature')

    geojson: Mapped[LineString] = mc(JSON)


def to_line_feature(ind_records, individual):
    """ Create a LineString GeoJSON Feature """

    props = LineProperties(ind_records, individual)
    coordinates = list(
        map(lambda record: (record.longitude, record.latitude), ind_records))

    geojson = Feature(geometry=LineString(
        coordinates), properties=props.__dict__)

    if geojson.is_valid:
        return geojson
