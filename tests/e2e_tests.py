""" End to end tests """

import os
from pathlib import Path
from flask import json, url_for
from playwright.sync_api import Browser, Page, expect
from ailerons_tracker_backend.db import db
from ailerons_tracker_backend.models.individual_model import Individual

PASSWORD = os.getenv("ADMIN_PWD")

# Overwrite browser state file to remove session cookies and test login
Path('./playwright/.auth/state.json').write_text(json.dumps({}))


def test_redirect_login(page: Page, app):
    """ Test that portal redirects to login page and that login manager
        redirects unauthenticated users to login page """

    with app.app_context():

        page.goto(url_for("portal.dashboard.show"))
        expect(page).to_have_url(url_for("portal.login.show"))

        page.goto(url_for("portal.csv.show"))
        expect(page).to_have_url(url_for("portal.login.show"))

        page.goto(url_for("portal.individual.show_create"))
        expect(page).to_have_url(url_for("portal.login.show"))


def test_login(page: Page, app, browser: Browser, browser_context_args):
    """ Test loging in and that the state file is updated with session cookie """

    with app.app_context():
        page.goto(url_for("portal.login.show"))

        assert PASSWORD is not None

        page.get_by_label("Mot de passe:").fill(PASSWORD)

        page.locator("[type=submit]").click()

        prev_state = json.load(browser_context_args["storage_state"].open("r"))
        assert prev_state == {}

        expect(page).to_have_url(
            url_for("portal.dashboard.show_table"), timeout=5000)

        # Write in state file
        browser.contexts[0].storage_state(path="./playwright/.auth/state.json")

        assert json.load(
            browser_context_args["storage_state"].open("r")) != prev_state


def test_new_ind_button(page: Page, app):

    with app.app_context():
        page.goto(url_for("portal.dashboard.show"))
        expect(page).to_have_url(
            url_for("portal.dashboard.show_table"), timeout=5000)

        page.locator("button", has_text="Ajouter").click(timeout=1000)
        expect(page).to_have_url(
            url_for("portal.individual.show_create"), timeout=5000)


def test_ind_form(page: Page, app):
    """ Test the form for adding a new individual,
        mainly attributes, values and HTMX """

    with app.app_context():
        page.goto(url_for("portal.individual.show_create"))

        form = page.locator("form#create-infocard-form")
        expect(form).to_have_attribute(
            "hx-post", url_for("portal.individual.create", _external=False))
        expect(form).to_have_attribute("hx-target", "#create-infocard-section")
        expect(form).to_have_attribute("hx-swap", "outerHTML")
        expect(form).to_have_attribute("hx-encoding", "multipart/form-data")

        expect(form.locator("input#csrf_token")).to_be_hidden()

        input_surnom = page.get_by_label("Surnom")
        expect(input_surnom).to_have_attribute("type", "text")
        expect(input_surnom).to_have_id("individual_name")
        expect(input_surnom).to_have_attribute("name", "individual_name")
        expect(input_surnom).to_be_empty()

        select_sexe = page.get_by_label("Sexe")
        expect(select_sexe).to_have_id("sex")
        expect(select_sexe).to_have_attribute("name", "sex")

        options = select_sexe.locator("option")
        expect(options).to_have_count(3)

        input_photos = page.get_by_label("Photos")
        expect(input_photos).to_have_attribute("type", "file")
        expect(input_photos).to_have_attribute("name", "pictures")
        expect(input_photos).to_have_attribute("accept", ".png,.jpg")


def test_context_form(page: Page, app):
    """ Test the context form for a new individual """

    with app.app_context():
        page.goto(url_for("portal.individual.show_create"))

        textarea_description = page.get_by_label("Description")
        expect(textarea_description).to_have_attribute("name", "description")
        expect(textarea_description).to_have_attribute(
            "placeholder", "Rédigez une courte description ici")

        input_size = page.get_by_label("Envergure à la pose")
        expect(input_size).to_have_attribute("type", "number")
        expect(input_size).to_have_attribute("name", "size")
        expect(input_size).to_have_attribute("min", "1")
        expect(input_size).to_have_attribute("max", "15")

        input_tag_date = page.get_by_label('Date de pose de balise')
        expect(input_tag_date).to_have_attribute("type", "datetime-local")
        expect(input_tag_date).to_have_attribute("name", "tag_date")

        textarea_behavior = page.get_by_label("Comportement observé")
        expect(textarea_behavior).to_have_attribute("name", "behavior")
        expect(textarea_behavior).to_have_attribute(
            "placeholder", "Rédigez vos observations ici")


def test_form_cancel(page: Page, app):
    """ Test cancelling adding a new individual """

    with app.app_context():
        page.goto(url_for("portal.individual.show_create"))

        button_cancel = page.locator("button", has_text="Annuler")
        expect(button_cancel).to_have_attribute(
            "hx-get", url_for("portal.dashboard.show", _external=False), timeout=5000)
        expect(button_cancel).to_have_attribute("hx-push-url", "true")
        expect(button_cancel).to_have_attribute("hx-trigger", "click")
        expect(button_cancel).to_have_attribute("hx-target", "main")
        expect(button_cancel).to_have_attribute(
            "hx-swap", "innerHTML swap:300ms settle:50ms show:window:top")

        button_cancel.click()
        expect(page).to_have_url(
            url_for("portal.dashboard.show_table"), timeout=10000)


def test_form_submit(page: Page, app):
    """ Test filling and sending the new individual form """

    # Make sure test ind does not exist
    with app.app_context():
        ind = db.session.execute(
            db.select(Individual).where(
                Individual.individual_name == "ind_name_pw")
        ).scalar()

        if ind is not None:
            db.session.delete(ind)
            db.session.commit()

        page.goto(url_for("portal.individual.show_create"))

        page.get_by_label("Surnom").fill("ind_name_pw")

        select_sex = page.get_by_label("Sexe")
        select_sex.click()

        select_sex.select_option("Femelle")
        expect(select_sex).to_have_value("Femelle")

        page.get_by_label("Description").fill("desc_pw")

        page.get_by_label("Envergure à la pose").fill("8")

        page.get_by_label("Date de pose de balise").fill("2020-01-01T12:00")

        radio_alone = page.get_by_label("Seul")
        radio_alone.click()
        expect(radio_alone).to_be_checked()

        page.get_by_label("Comportement observé").fill("behavior_pw")

        page.locator("input.submit").click()
        expect(page).to_have_url(url_for("portal.dashboard.show_table"))

        cell_new_individual_name = page.get_by_role(
            "row").get_by_role("cell").get_by_text("ind_name_pw")

        expect(cell_new_individual_name).to_be_visible()


def test_csv(page: Page,  app):
    """ Test accessing the CSV upload form """

    with app.app_context():
        test_ind_id = db.session.execute(db.select(
            Individual.id
        ).where(Individual.individual_name == "ind_name_pw")).one()[0]

        page.goto(url_for("portal.dashboard.show"))

        csv_get = url_for("portal.csv.show", id=test_ind_id, _external=False)
        button_upload_first = page.locator(f'[hx-get="{csv_get}"]')
        button_upload_first.click()

        expect(page).to_have_url(url_for("portal.csv.show", id=test_ind_id))

        input_file_locs = page.get_by_label("Relevés de localisation")
        expect(input_file_locs).to_have_attribute("type", "file")
        expect(input_file_locs).to_have_attribute("accept", ".csv")
        expect(input_file_locs).to_have_attribute("name", "loc_file")

        input_file_depth = page.get_by_label("Relevés de profondeur")
        expect(input_file_depth).to_have_attribute("type", "file")
        expect(input_file_depth).to_have_attribute("accept", ".csv")
        expect(input_file_depth).to_have_attribute("name", "depth_file")


def test_submit_csv(page: Page, app, resources):
    """ Test selecting files and submitting form """

    with app.app_context():
        page.goto(url_for("portal.dashboard.show"))
        page.wait_for_url(url_for("portal.dashboard.show_table"), timeout=5000)

        page.locator("button", has_text="Upload").nth(0).click()

        page.get_by_label("Relevés de localisation").set_input_files(
            resources / "gpe3.csv")
        page.get_by_label("Relevés de profondeur").set_input_files(
            resources / "series.csv")
        page.locator("[type=submit]").click()

        expect(page).to_have_url(
            url_for("portal.dashboard.show_table"), timeout=15000)
