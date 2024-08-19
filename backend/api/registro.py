from flask import Blueprint, request, redirect, url_for
from backend.helpers.mail import enviar_mail
from backend.helpers.produccion import conseguir_url
from backend.models.usuario import (
    crear_usuario,
    buscar_usuario_por_email,
    completar_usuario,
    buscar_usuario_por_username,
)

registro_bp = Blueprint("registro", __name__, url_prefix="/autenticacion/registro")


@registro_bp.post("/")
def registro_simple():
    """
    Muestra la vista de la primera etapa del registro, además valida los
    parametros, envia el mail de confirmación y guarda al usuario si
    se recibió el formulario.
    """
    # validar con schema
    if buscar_usuario_por_email():
        flash("El mail ingresado ya se encuentra registrado", "error")
        return redirect(url_for("registro"))

    crear_mail(email, form.nombre.data, form.apellido.data)
    crear_usuario(nombre, apellido, email, token)

    flash(
        "Se envió un mail de confirmación a su email para finalizar el registro.",
        "success",
    )
    return redirect(url_for("acceso.login"))


@registro_bp.route("/confirmar", methods=["GET", "POST"])
def confirmar_registro():
    """
    Termina el registro del usuario estableciendo una contraseña.
    """

    # sanitizar data y validar con schema
    completar_usuario(email, form.username.data, form.password.data)

    flash("Ha finalizado su registro, puede usar su cuenta.", "success")
    return redirect(url_for("acceso.login"))


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
""".format(
        conseguir_url(), email, token
    )

    enviar_mail("Confirmación de cuenta", email, html=html)
