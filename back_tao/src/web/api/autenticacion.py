from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
)
from werkzeug.exceptions import UnsupportedMediaType

from src.core.autenticacion import chequear_usuario, buscar_usuario_por_email, es_dueño, es_superadmin
from src.web.schemas.autenticacion import autenticacion_schema
from marshmallow import ValidationError

api_autenticacion_bp = Blueprint("autenticacion_api", __name__, url_prefix="/api/auth")


@api_autenticacion_bp.post("/")
def auth():
    """Devuelve el jwt recibiendo email y password por json"""

    try:
        req_data = request.json
    except UnsupportedMediaType:
        return {
            "error": "Debe proveer email y password en el contenido json de la peticion"
        }, 400

    try:
        data_validada = autenticacion_schema.load(req_data)
    except ValidationError:
        return jsonify({"error": "Parametros invalidos"}), 400

    user = chequear_usuario(data_validada["email"], data_validada["password"])
    if not user:
        return jsonify({"error": "Usuario y/o contraseña invalidos"}), 401

    es_admin = es_dueño(user.email) != None or es_superadmin(user.email) != None

    access_token = create_access_token(identity=user.id, additional_claims={ "es_admin": es_admin, "id": user.id })
    response = jsonify({"token": access_token})
    set_access_cookies(response, access_token)

    return response, 200


@api_autenticacion_bp.get("/logout")
@jwt_required()
def logout_jwt():
    response = jsonify()
    unset_jwt_cookies(response)
    return response, 200
