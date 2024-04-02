""" Individual data upload blueprint """

from jinja2 import TemplateNotFound
from jinja_partials import render_partial
import postgrest
from flask import Blueprint, abort, request, current_app
from ailerons_tracker_backend.errors import InvalidFile
from ailerons_tracker_backend.upload_image import upload_image
from ailerons_tracker_backend.models.individual_model import Individual, Context
from ailerons_tracker_backend.clients.supabase_client import supabase

individual_infos = Blueprint('individual_infos', __name__,
                             template_folder='templates')


@individual_infos.post('/individual')
def create_individual():
    """ Create a new row in table individual """
    try:
        items = request.files.items(multi=True)
        image_urls = []

        for item in items:
            image_url = upload_image(item[1])
            image_urls.append(image_url)

        ind_data = Individual(
            request.form["indName"],
            request.form["indSex"],
            image_urls,
            description=request.form["indDesc"]).upload()

        ind_id = ind_data.get('id')
        context_data = Context(individual_id=ind_id,
                               date=request.form["tagDate"],
                               situation=request.form["situation"],
                               size=request.form["indSize"],
                               behavior=request.form["indBehavior"]).upload()
        content = {
            'message': 'Successfully uploaded new individual',
            'Individual data': ind_data,
            'Context': context_data
        }

        current_app.logger.warning(content)
        individuals = supabase.get_all('individual_new')
        return render_partial('dashboard/individual_table.jinja', inds=individuals), 200

    except postgrest.exceptions.APIError as e:
        current_app.logger.error(e.message)
        return e.message, 304

    except InvalidFile as e:
        current_app.logger.error(e.message)
        return e.message, 400


@individual_infos.get('/new_individual')
def show():
    """ Get new individual window """
    try:
        return render_partial('individual_infos/individual_infos.jinja')
    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)


@individual_infos.get('/edit_individual')
def edit():
    """ Return edit window """
    try:
        individual_id = request.args.get("id")
        individual = supabase.get_match(
            "id", individual_id, "individual_new")[0]
        current_app.logger.warning(individual)
        context = supabase.get_match(
            "individual_id", individual_id, "context")[0]
        current_app.logger.warning(context)
        return render_partial('individual_infos/individual_infos_edit.jinja', ind=individual, context=context)

    except TemplateNotFound as e:
        current_app.logger.warning(e)
        abort(404)
