from flask import Blueprint, render_template
from src.core.models import prueba

prueba_blueprint = Blueprint("pruebas", __name__, url_prefix="/pruebas")

@prueba_blueprint.get("/")
def prueba_index():
    return render_template("prueba.html", pruebas=prueba.list_pruebas())