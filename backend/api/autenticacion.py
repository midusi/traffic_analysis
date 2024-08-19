from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    get_jwt_identity,
)
from werkzeug.exceptions import UnsupportedMediaType
from backend.models.usuario import chequear_usuario, buscar_usuario_por_id, es_admin
from backend.models.schemas.autenticacion import autenticacion_schema, perfil_schema
from marshmallow import ValidationError

api_autenticacion_bp = Blueprint("auth", __name__, url_prefix="/auth")


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

    admin = es_admin(user.email)

    access_token = create_access_token(
        identity=user.id, additional_claims={"es_admin": admin, "id": user.id}
    )
    response = jsonify({"token": access_token})
    set_access_cookies(response, access_token)

    return response, 200


@api_autenticacion_bp.get("/logout")
@jwt_required()
def logout_jwt():
    response = jsonify()
    unset_jwt_cookies(response)
    return response, 200


@api_autenticacion_bp.get("/me")
@jwt_required()
def profile():
    """Devuelve los datos del usuario autenticado"""

    id_usuario = get_jwt_identity()
    usuario = buscar_usuario_por_id(id_usuario)
    datos = perfil_schema.dump(usuario)
    response = jsonify(datos)

    return response, 200
