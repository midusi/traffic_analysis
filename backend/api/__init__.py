from flask import Blueprint
from backend.api.prueba import prueba_blueprint
# Blueprint principal para la api
api_blueprint = Blueprint("api", __name__, url_prefix="/api/")

# Anidamos los blueprints
api_blueprint.register_blueprint(prueba_blueprint)
