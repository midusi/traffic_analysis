from flask import Blueprint
from backend.api.prueba import prueba_blueprint
from .autenticacion import api_autenticacion_bp
from .registro import registro_bp

# Blueprint principal para la api
api_blueprint = Blueprint("api", __name__, url_prefix="/api/")

# Anidamos los blueprints
api_blueprint.register_blueprint(prueba_blueprint)
api_blueprint.register_blueprint(api_autenticacion_bp)
api_blueprint.register_blueprint(registro_bp)
