""" Supabase Client test suite """
from pathlib import Path
import postgrest
import pytest

from ailerons_tracker_backend.clients.supabase_client import SupabaseClient
from ailerons_tracker_backend.geojson_generator.data_classes.feature_models import PointFeature

supabase = SupabaseClient()

resources = Path(__file__).parent / "resources"


def test_init():
    """ Test if client was instaciated """
    assert supabase


def test_get_all():
    """ Test querying for all table entries"""
    assert isinstance(supabase.get_all("individual"), list)


def test_get_match():
    """ Test querying for specific matching rows """
    res = supabase.get_match("id", "1", "individual")
    assert isinstance(res, list)


def test_get_individual_ids():
    """ Test querying for a list of all ind. IDs """
    data = supabase.get_individual_ids()
    assert isinstance(data, list)


recs = supabase.get_all("record")
inds = supabase.get_all("individual")

test_point = PointFeature(recs[0], inds[0])


class TestUpsertFeature():
    """ Test inserting or updating a row in table 'point' """

    def test_valid_type(self):
        """ Test inserting in feature table """

        res = supabase.upsert(test_point, 'point_geojson')

        assert isinstance(res, dict)

    def test_invalid_type(self):
        """ Test attempting insert in wrong table """

        with pytest.raises(postgrest.exceptions.APIError):
            supabase.upsert(test_point, 'individual')
