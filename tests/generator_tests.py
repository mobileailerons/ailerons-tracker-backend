""" Generator test suite """

import logging
from geojson import FeatureCollection
from python_mts.scripts.mts_handler import MtsHandler
from ailerons_tracker_backend.geojson_generator.data_classes.feature_models import LineStringFeature, PointFeature
from ailerons_tracker_backend.geojson_generator.generator import Generator

mts = MtsHandler()
generator = Generator()


def test_init():
    """ Test instanciation of generator """
    assert isinstance(generator, Generator)


def test_generate():
    """ Test generating geoJSON features from DB """
    generator.generate()

    assert isinstance(generator.get_lines()[0], LineStringFeature)

    assert isinstance(generator.get_points()[0][0], PointFeature)

    assert isinstance(generator.get_p_collections()[0], FeatureCollection)
