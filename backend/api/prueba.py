from flask import jsonify, make_response, Blueprint, request
from backend.models import prueba
from backend.models.schemas.prueba import prueba_schema

prueba_blueprint = Blueprint("prueba", __name__, url_prefix="/prueba")

@prueba_blueprint.get("/")
def get_all_pruebas():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=1, type=int)

    pruebas = prueba.list_pruebas(page=page, per_page=per_page)

    data = {
        "pruebas": prueba_schema.dump(pruebas),
        "page": pruebas.page,
        "cantPages": pruebas.pages,
        "has_next": pruebas.has_next,
        "has_prev": pruebas.has_prev,
        "first": pruebas.first,
        "last": pruebas.last,
        "total": pruebas.total
    }

    return make_response(jsonify(data))