""" Test suite for image upload """

import logging
from datetime import date
from pathlib import Path
from ailerons_tracker_backend.models.individual_model import Individual
from ailerons_tracker_backend.db import db
resources = Path(__file__).parent / "resources"


def test_client(client):
    """ Test if conf file provides client for mocking API requests """
    assert client


def test_new_individual_route(app, client):
    """ Test individual route by mocking a request """

    with app.app_context():
        ind = db.session.execute(
            db.select(
                Individual
            ).where(Individual.individual_name == 'Poupette')).scalar()

        if isinstance(ind, Individual):
            db.session.delete(ind)

            db.session.commit()

        response = client.post(
            "/portal/individual/new",
            data={
                "individual_name": 'Poupette',
                "sex": 'Femelle',
                "picture": (
                    resources / "test.png").open("rb"),
                "description": '...',
                "behavior": 'Complétement zinzin celle là.',
                "size": 8,
                "situation": 'Seul',
                "date": date.today().isoformat(),
            })

        assert response.status_code == 200


def test_edit_individual_route(app, client):
    """ Test individual route by mocking a request """

    with app.app_context():
        ind = db.session.execute(
            db.select(
                Individual
            ).where(Individual.individual_name == 'Poupette')).scalar()

        db.session.commit()

        response = client.post(
            f"/portal/individual/edit?id={ind.id}",
            data={
                "description": '... pas sérieux.'}
        )

        assert response.status_code == 200


def test_upload_route(client, app):
    """ Test upload route by mocking a request """

    with app.app_context():
        ind = db.session.execute(
            db.select(
                Individual
            ).where(Individual.individual_name == 'Poupette')).scalar()

        response = client.post(
            f"/portal/csv/upload?id={ind.id}",

            data={
                "loc_file": (resources / "gpe3.csv").open("rb"),
                "depth_file": (resources / "series.csv").open("rb")})

        logging.error(response)
        assert response.status_code == 200


def test_portal_route(client):
    """ Test portal route """

    response = client.get("/portal")
    assert response.status_code == 308


def test_dashboard_route(client):
    """ Test dashboard route in the context of a regular request """

    response = client.get("/portal/dashboard")
    assert response.status_code == 200


def test_dashboard_route_htmx(client):
    """ Test dashboard route in the context of an htmx request """

    headers = {'HTTP_HX-Request': 'true'}
    response = client.get("/portal/dashboard", headers=headers)

    assert response.status_code == 200
