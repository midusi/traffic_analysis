from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    get_jwt_identity,
)
from werkzeug.exceptions import UnsupportedMediaType
from backend.models.usuario import (
    chequear_usuario,
    buscar_usuario_por_id,
    buscar_usuario_por_email,
    es_admin,
    renovar_password,
    renovar_token,
)
from backend.models.schemas.autenticacion import autenticacion_schema, perfil_schema
from backend.models.schemas.registro import (
    confirmar_registro_schema,
    recuperar_contraseña_schema,
)
from marshmallow import ValidationError
from backend.helpers.produccion import conseguir_url
from backend.helpers.mail import enviar_mail

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


@api_autenticacion_bp.post("/recuperar_password")
def recuperar_password():
    """Envia un mail al usuario autenticado con un token para cambiar la contraseña"""

    try:
        req_data = request.json
    except UnsupportedMediaType:
        return {"error": "Debe proveer email en el contenido json de la peticion"}, 400

    try:
        data_validada = recuperar_contraseña_schema.load(req_data)
    except ValidationError:
        return jsonify({"error": "Parametros invalidos"}), 400

    usr = buscar_usuario_por_email(data_validada["email"])
    token = renovar_token(usr.id)  # Renueva el token valido para 24hrs
    crear_mail(usr.email, token)

    return jsonify({"message": "Se envió un mail de recuperación a su email"}), 200


@api_autenticacion_bp.post("/cambiar_password")
def cambiar_password():
    """Cambia la contraseña del usuario, en la url llega como parametro email y token"""

    try:
        data_validada = confirmar_registro_schema.load(request.args)
    except ValidationError:
        return (
            jsonify(
                {
                    "error": "Parametros invalidos, debe proporcionar email y password que cumplan los requisitos"
                }
            ),
            400,
        )

    usuario = buscar_usuario_por_id(id_usuario)
    renovar_password(usuario.email, data_validada["password"], usuario.token)

    return jsonify({"message": "Contraseña actualizada"}), 200


def crear_mail(email, token):
    html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            color: #333;
            padding: 20px;
        }}

        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #fff;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}

        h1 {{
            color: #007bff;
        }}

        p {{
            line-height: 1.6;
        }}

        a {{
            color: #007bff;
            text-decoration: none;
            font-weight: bold;
        }}

        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1> Reestablece tu contraseña </h1>
        <p>Hacé click en el siguiente enlace para recuperar la contraseña (valido por 24hrs):</p>
        <p><a href="{0}/auth/registro/recuperar_password?email={1}&token={2}">Confirmar</a></p>
    </div>
</body>
</html>
""".format(
        conseguir_url(), email, token
    )

    enviar_mail("Confirmación de cuenta", email, html=html)
