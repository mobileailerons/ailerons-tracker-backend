""" Individual data upload blueprint """

import postgrest
import flask_login
from flask_htmx import HTMX, make_response
from jinja2 import TemplateNotFound
from jinja_partials import render_partial
from flask import Blueprint, abort, flash, render_template, request, current_app
from werkzeug.datastructures import FileStorage, iter_multi_items
from wtforms.validators import ValidationError
from ailerons_tracker_backend.db import db
from ailerons_tracker_backend.clients import cloudinary_client
from ailerons_tracker_backend.errors import InvalidFile
from ailerons_tracker_backend.models.individual_model import Individual
from ailerons_tracker_backend.models.context_model import Context
from ailerons_tracker_backend.forms.individual_forms import ContextForm, IndividualForm
from ailerons_tracker_backend.models.picture_model import Picture

individual_infos = Blueprint('individual_infos', __name__,
                             template_folder='templates', url_prefix='individual')


def upload_images(files: list[FileStorage]) -> list[str]:
    """ Parse and upload image files.

    Args:
        files (list[FileStorage]): form data (request file objects) that might also have been populated with existing row data (URL strings) """

    image_urls = []

    for k, v in iter_multi_items(files):
        image_url = cloudinary_client.upload(v.filename, v)
        image_urls.append(image_url)

    return image_urls


@ individual_infos.post('/edit')
@ flask_login.login_required
def update_individual():
    """ Update specific rows in tables individual and context """

    try:
        ind_id = request.args.get("id", type=int)

        if not ind_id:
            raise ValueError()

        ind = db.session.get_one(Individual, ind_id)

        ind_form = IndividualForm(obj=ind)
        context_form = ContextForm(obj=ind.context)

        ind_form.validate()
        context_form.validate()

        ind_form.populate_obj(ind)
        context_form.populate_obj(ind.context)

        if request.files:
            image_urls: list[str] = upload_images(request.files)
            for url in image_urls:
                ind.picture.append(Picture(url=url))

        db.session.add(ind)
        db.session.commit()

        content = {
            'message': f'Successfully updated individual {ind.id}',
            'individual_data': ind,
            'context_data': ind.context}

        current_app.logger.info(content)
        flash(content['message'])

        individuals = db.session.execute(
            db.select(
                Individual)).scalars().all()

        return make_response(
            render_partial('dashboard/dashboard.jinja', inds=individuals),
            push_url='/portal/dashboard'), 200

    except ValidationError as e:
        current_app.logger.warning(e)
        return e, 400

    except InvalidFile as e:
        current_app.logger.error(e.message)
        return e.message, 400

    except postgrest.exceptions.APIError as e:
        current_app.logger.error(e.message)
        return e.message, 304


@ individual_infos.post('/new')
@ flask_login.login_required
def create_individual():
    """ Create new rows in tables individual and context """

    try:
        ind_form = IndividualForm()
        context_form = ContextForm()

        ind_form.validate()
        context_form.validate()

        ind = Individual(
            individual_name=ind_form.individual_name.data,
            sex=ind_form.sex.data,
            description=ind_form.description.data,
            context=Context(size=context_form.size.data,
                            behavior=context_form.behavior.data,
                            situation=context_form.situation.data,
                            date=context_form.date.data)
        )

        if request.files:
            image_urls: list[str] = upload_images(request.files)
            for url in image_urls:
                ind.picture.append(Picture(url=url))

        db.session.add(ind)
        db.session.commit()

        content = {'message': f'Successfully created new individual {ind.id}',
                   'individual_data': ind,
                   'context_data': ind.context}

        current_app.logger.info(content)

        flash(content['message'])

        individuals = db.session.execute(db.select(Individual)).scalars()

        return make_response(
            render_partial(
                'dashboard/dashboard.jinja', inds=individuals),
            replace_url='portal/dashboard'), 200

    except ValidationError as e:
        current_app.logger.warning(e)
        return e, 400

    except InvalidFile as e:
        current_app.logger.error(e.message)
        return e.message, 400

    except postgrest.exceptions.APIError as e:
        current_app.logger.error(e.message)
        return e.message, 304


@ individual_infos.get('/new')
@ flask_login.login_required
def show():
    """ Serve the view to create a new individual """

    htmx = HTMX(current_app)
    form = IndividualForm()

    try:
        current_app.logger.debug("YO")
        if htmx:
            return render_partial('individual_infos/individual_infos.jinja', form=form)

        return render_template(
            'base_layout.jinja', view='new', form=form)

    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)


@ individual_infos.get('/edit')
@ flask_login.login_required
def edit():
    """ Serve the view to edit an individual """

    htmx = HTMX(current_app)
    form = IndividualForm()

    try:
        ind_id = request.args.get("id")

        if ind_id:
            ind = db.session.get_one(Individual, ind_id)

        else:
            current_app.logger.warning(f"No individual found for ID={ind_id}")
            abort(404)

        if htmx:
            return render_partial(
                'individual_infos/individual_infos_edit.jinja', ind=ind, form=form)

        return render_template(
            'base_layout.jinja',
            view=f'edit?id={ind_id}',
            form=form)

    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)
