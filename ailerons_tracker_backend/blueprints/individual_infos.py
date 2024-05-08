""" Individual data upload blueprint """

from flask_htmx import HTMX, make_response
import flask_login
from jinja2 import TemplateNotFound
from jinja_partials import render_partial
import postgrest
from flask import Blueprint, abort, flash, render_template, request, current_app
from ailerons_tracker_backend.clients import cloudinary_client
from ailerons_tracker_backend.errors import InvalidFile
from ailerons_tracker_backend.models.individual_model import Individual
from ailerons_tracker_backend.models.context_model import Context
from ailerons_tracker_backend.clients.supabase_client import supabase
from ailerons_tracker_backend.forms.individual_forms import NewIndividualForm, EditIndividualForm

individual_infos = Blueprint('individual_infos', __name__,
                             template_folder='templates', url_prefix='individual')


def upload_images(files):
    """ Parse and upload image files """

    image_urls = []

    for file in files:
        image_url = cloudinary_client.upload(file.filename, file)
        image_urls.append(image_url)

    return image_urls


@ individual_infos.post('/edit')
@ flask_login.login_required
def update_individual():
    """ Update a specific row in tables individual and context"""

    try:
        ind_id = request.args.get("id")
        form = EditIndividualForm()
        current_app.logger.warning(form.validate())
        if form.validate():
            ind = Individual.get_from_db(ind_id)
            context = Context.get_with_ind_id(ind_id)

            if form.images.data:
                image_urls: list[str] = upload_images(form.images.data)
                ind.pictures = image_urls

            form.populate_obj(ind)
            form.populate_obj(context)

            ind.upload()
            context.upload()

            content = {
                'message': f'Successfully updated individual {ind.id}',
                'individual_data': ind.to_dict(),
                'context_data': context.to_dict()}

            flash(content['message'])

            individuals = Individual.get_all()
            current_app.logger.warning(individuals)

            return make_response(
                render_partial('dashboard/dashboard.jinja',
                               inds=individuals),
                push_url='dashboard'), 200

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
        form = NewIndividualForm()
        current_app.logger.warning(form.validate())
        if form.validate():
            current_app.logger.warning('YYYYYYYOOOOO')
            ind = Individual(name=form.name.data,
                             sex=form.sex.data,
                             description=form.data.description)

            if form.images.data:
                image_urls: list[str] = upload_images(form.images.data)
                ind.pictures = image_urls

                ind.upload()

                context = Context.get_with_ind_id(ind.id)
                context.upload()

                content = {'message': f'Successfully created new individual {ind.id}',
                           'individual_data': ind.to_dict(),
                           'context_data': context.to_dict()}

                current_app.logger.warning(content)

                flash(content['message'])

                individuals = Individual.get_all()

                return make_response(
                    render_partial('dashboard/dashboard.jinja',
                                   inds=individuals),
                    push_url='dashboard'), 200

    except InvalidFile as e:
        current_app.logger.error(e.message)
        return e.message, 400

    except postgrest.exceptions.APIError as e:
        current_app.logger.error(e.message)
        return e.message, 304


@ individual_infos.get('/new')
@ flask_login.login_required
def show():
    """ Get new individual window """
    htmx = HTMX(current_app)
    try:
        if htmx:
            return make_response(render_partial('individual_infos/individual_infos.jinja'),
                                 push_url="new_individual")

        return render_template('base_layout.jinja', view='new_individual')

    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)


@ individual_infos.get('/edit')
@ flask_login.login_required
def edit():
    """ Return edit window """
    htmx = HTMX(current_app)

    try:
        ind_id = request.args.get("id")
        if ind_id:
            ind = supabase.get_exact(
                "id", ind_id, "individual")

            context = supabase.get_exact(
                "individual_id", ind_id, "context")
        else:
            raise ValueError

        if htmx:
            return make_response(
                render_partial('individual_infos/individual_infos_edit.jinja',
                               ind=ind,
                               context=context),
                push_url=f"edit_individual?id={ind_id}")

        return render_template('base_layout.jinja', view=f'edit_individual?id={ind_id}')

    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)
