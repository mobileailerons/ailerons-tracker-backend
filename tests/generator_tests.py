""" Generator test suite """
from ailerons_tracker_backend.geojson_generator.generator import generator, Generator

def test_init():
    """ Test instanciation of generator """
    assert isinstance(generator, Generator)
