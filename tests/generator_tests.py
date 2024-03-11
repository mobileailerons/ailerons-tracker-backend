""" Generator test suite """

import json
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


def test_generate_geojson():
    """ Test generating geoJSON features from DB """
    generator.generate_geojson()

    assert isinstance(generator.get_lines()[0], LineStringFeature)

    assert isinstance(generator.get_points()[0][0], PointFeature)

    assert isinstance(generator.get_p_collections()[0], FeatureCollection)


def test_write_recipe():
    """ test creating or updating a tileset recipe file """

    rcp_dict = {"version": 1,
                "layers": {
                    "trees": {
                        "source": "mapbox://tileset-source/louiscoutel/test",
                        "minzoom": 4, "maxzoom": 8
                    }
                }
                }

    generator.write_recipe(rcp_dict, "test_recipe.json")

    with open("test_recipe.json", mode="r", encoding="utf-8") as f:
        file_dict = json.load(f)
        assert file_dict == rcp_dict
