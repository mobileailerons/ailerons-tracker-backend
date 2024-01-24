""" Generator test suite """
from ..generator import generator, Generator

def test_init():
    """ Test instanciation of generator """
    assert isinstance(generator, Generator)
