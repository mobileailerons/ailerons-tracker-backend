""" Transfrom database entries into geoJSON files """
import logging
import geojson
from ailerons_tracker_backend.errors import GeneratorLineError, GeneratorPointError
from ailerons_tracker_backend.models.feature_models import LineGeojson, to_point_feature, PointGeojson, to_line_feature


def generate(individual, db):

    features: list[geojson] = []

    try:
        for record in individual.records:
            point = PointGeojson(
                individual_id=individual.id,
                record_id=record.id,
                geojson=to_point_feature(record, individual))
            record.point_feature = point

            features.append(point.geojson)

    except Exception as e:
        raise GeneratorPointError(individual, e) from e

    try:
        individual.line_feature = LineGeojson(individual_id=individual.id,
                                              geojson=to_line_feature(individual.records, individual))

    except Exception as e:
        raise GeneratorLineError(individual.records, e) from e

    individual.feature_collection = geojson.FeatureCollection(features)

    db.session.add(individual)
    db.session.commit()
