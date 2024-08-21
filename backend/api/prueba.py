from flask import jsonify, make_response, Blueprint
from backend.models import prueba
from backend.models.schemas.prueba import prueba_schema

prueba_blueprint = Blueprint("prueba", __name__, url_prefix="/prueba")

@prueba_blueprint.get("/")
def get_all_pruebas():
    pruebas = prueba.list_pruebas()
    return make_response(jsonify(prueba_schema.dump(pruebas)))