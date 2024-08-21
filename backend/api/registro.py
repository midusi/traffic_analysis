from flask import Blueprint, jsonify, request
from backend.helpers.mail import enviar_mail
from backend.helpers.produccion import conseguir_url
from backend.models.usuario import (
    crear_usuario,
    buscar_usuario_por_email,
    renovar_password,
)
from backend.models.schemas.registro import (
    registro_schema,
    renovar_contraseña_schema,
)
from marshmallow import ValidationError
import secrets
from werkzeug.exceptions import UnsupportedMediaType

registro_bp = Blueprint("registro", __name__, url_prefix="/registro")


@registro_bp.post("/")
def registro():
    """
    Valida los parametros y envia el mail de confirmación
    """

    try:
        req_data = request.json
    except UnsupportedMediaType:
        return {
            "error": "Debe proveer nombre, apellido, email y si es admin en el contenido json de la peticion"
        }, 400

    try:
        data = registro_schema.load(req_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    if buscar_usuario_por_email(data["email"]):
        return jsonify({"error": "El mail ingresado ya se encuentra registrado."}), 422

    random = secrets.token_urlsafe(16)
    usr = crear_usuario(
        nombre=data["nombre"],
        apellido=data["apellido"],
        email=data["email"],
        admin=data["admin"],
        password=random,  # setea una contraseña cualquiera para impedir el acceso sin haber verificado el mail
    )
    crear_mail(data["email"], usr.token)

    return (
        jsonify(
            {
                "message": "Se envió un mail de confirmación a su email para finalizar el registro."
            }
        ),
        200,
    )


@registro_bp.post("/confirmar")
def confirmar_registro():
    """
    Termina el registro del usuario estableciendo una contraseña. Recibe el token y la contraseña en el body.
    """

    try:
        req_data = request.json
    except UnsupportedMediaType:
        return {
            "error": "Debe proveer token y password en el contenido json de la peticion"
        }, 400

    try:
        data = renovar_contraseña_schema.load(req_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    valid = renovar_password(password=data["password"], token=data["token"])
    if not valid:
        return (
            jsonify({"error": "El token de confirmación es inválido o ha expirado."}),
            422,
        )

    return ({"message": "Ha finalizado su registro, puede usar su cuenta."}), 200


def crear_mail(email, token):
    """
    Crea un usuario con los datos recibidos y manda un mail de confirmación.
    El token es un codigo aleatorio de un solo uso que va a ir en la URL de confirmación.
    """

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
        <h1> Ha sido registrado en el sistema 🤝</h1>
        <p>Establecé una contraseña y terminá el registro usando el siguiente link:</p>
        <p><a href="{0}/auth/registro/confirmar?email={1}&token={2}">Confirmar</a></p>
    </div>
</body>
</html>
""".format(conseguir_url(), email, token)

    enviar_mail(asunto="Confirmación de cuenta", destinatario=email, html=html)
