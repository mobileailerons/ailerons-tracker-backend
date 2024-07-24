""" Generator test suite """

from ailerons_tracker_backend.db import db
from ailerons_tracker_backend.generator import generate
from ailerons_tracker_backend.models.individual_model import Individual


def test_generate(app):
    """ Test generating geoJSON features from DB """

    with app.app_context():
        individual = db.session.execute(
            db.select(Individual).where(
                Individual.individual_name == "Poupette")
        ).scalar()

        assert isinstance(individual, Individual)
        assert generate(individual, db).feature_collection is not None
        assert generate(individual, db).line_feature is not None
        assert generate(individual, db).records[0].point_feature is not None
