from flask import Blueprint, render_template, request, redirect, url_for, flash
from core.autenticacion.mail import enviar_mail
from src.web.helpers.autenticacion import no_necesita_login
from src.web.helpers.produccion import conseguir_url
from src.core.autenticacion import (
    buscar_usuario_por_email,
    crear_usuario_simple,
    completar_usuario,
    buscar_usuario_por_username,
)
from src.core.autenticacion.formularios import RegistroSimpleForm, ConfirmarRegistroForm

registro_bp = Blueprint("registro", __name__, url_prefix="/autenticacion/registro")


@registro_bp.route("/", methods=["GET", "POST"])
@no_necesita_login()
def registro_simple():
    """
    Muestra la vista de la primera etapa del registro, además valida los
    parametros, envia el mail de confirmación y guarda al usuario si
    se recibió el formulario.
    """
    form = RegistroSimpleForm()
    if form.validate_on_submit():
        if buscar_usuario_por_email(form.email.data):
            flash("El mail ingresado ya se encuentra registrado", "error")
            return redirect(url_for("registro.registro_simple"))

        crear_usuario_mandar_mail(form.email.data, form.nombre.data, form.apellido.data)

        flash(
            "Se envió un mail de confirmación a su email para finalizar el registro.",
            "success",
        )
        return redirect(url_for("acceso.login"))

    return render_template("autenticacion/registro.html", form=form)


@registro_bp.route("/confirmar", methods=["GET", "POST"])
def confirmar_registro():
    """
    Termina el registro del usuario, pidiendo en un formulario username y pass
    Se valida que no sea un mail invalido y que el username no esté tomado,
    además de las validaciones de los campos del formulario.
    """
    form = ConfirmarRegistroForm()
    if form.validate_on_submit():
        email = request.form.get("email")
        if not buscar_usuario_por_email(email):
            flash("Ese email no existe o no se encontró.", "error")
            return redirect(url_for("acceso.login"))

        if buscar_usuario_por_username(form.username.data):
            flash("Ese nombre de usuario ya está en uso", "error")
            return redirect(url_for("acceso.login"))

        completar_usuario(email, form.username.data, form.password.data)

        flash("Ha finalizado su registro, puede usar su cuenta.", "success")
        return redirect(url_for("acceso.login"))

    return render_template(
        "autenticacion/confirmar-registro.html", form=form, email=request.args["email"]
    )


def crear_usuario_mandar_mail(email, nombre, apellido):
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
        <h1>¡Gracias por registrarte! 🤝</h1>
        <p>Para continuar con tu registro, haz clic en el siguiente enlace:</p>
        <p><a href="{0}/autenticacion/registro/confirmar?email={1}">Confirmar</a></p>
    </div>
</body>
</html>
""".format(conseguir_url(), email)


    try:
        enviar_mail("Confirmación de cuenta", email, html=html)
    except Exception as err:
        flash("Hubo un error al enviar el mail.", "error")
        print(err)

    crear_usuario_simple(nombre, apellido, email)
