""" Model tests """
from datetime import date
from ailerons_tracker_backend import db
from ailerons_tracker_backend.models.individual_model import Individual
from ailerons_tracker_backend.models.context_model import Context


def test_create_ind(app):
    """ Test creating and inserting ind and context """

    with app.app_context():
        ind = db.session.execute(
            db.select(
                Individual,
                Context).join(
                Individual.context).where(
                Individual.individual_name == "Test")
        ).scalar()

        if isinstance(ind, Individual):
            db.session.delete(ind)
            db.session.commit()

        ind = Individual(
            individual_name="Test",
            sex="Femelle",
            picture=[],
            description='...',
            context=Context(
                date=date.today().isoformat(),
                situation='Seul',
                behavior='...',
                size=8)
        )

        db.session.add(ind)
        db.session.commit()

        assert db.session.get(Individual, ind.id) == ind


def test_upd_ind(app):
    """ Test update ind and context """

    with app.app_context():
        ind = db.session.execute(
            db.select(
                Individual,
                Context).join(
                Individual.context).where(
                Individual.individual_name == "Test")
        ).scalar()

        check = ind.sex

        ind.sex = 'Male' if ind.sex == 'Femelle' else 'Femelle'
        db.session.commit()

        check2 = db.session.execute(
            db.select(
                Individual.sex).where(
                Individual.id == ind.id)
        ).scalar()

        assert check != check2
