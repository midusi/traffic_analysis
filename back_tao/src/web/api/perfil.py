from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.core.autenticacion import buscar_usuario_por_id
from src.web.schemas.perfil import perfil_schema

api_perfil_bp = Blueprint("perfil_api", __name__, url_prefix="/api")


@api_perfil_bp.get("/me/profile")
@jwt_required()
def profile():
    """Devuelve los datos del usuario autenticado"""

    id_usuario = get_jwt_identity()
    usuario = buscar_usuario_por_id(id_usuario)
    datos = perfil_schema.dump(usuario)
    response = jsonify(datos)

    return response, 200
