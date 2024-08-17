from core import autenticacion
from flask import Blueprint, redirect, url_for, flash, session, render_template
from src.core.autenticacion.formularios import LoginForm
from src.web.helpers.autenticacion import necesita_login, no_necesita_login
from src.core.autenticacion import esta_activo, buscar_usuario_por_email

acceso_bp = Blueprint("acceso", __name__, url_prefix="/autenticacion/acceso")


@acceso_bp.route("/login", methods=["GET", "POST"])
@no_necesita_login()
def login():
    """
    Realiza el login, muestra el formulario si es un get, sino valida al usuario
    e inicia la sesión.
    """
    form = LoginForm()
    if form.validate_on_submit():
        if not buscar_usuario_por_email(form.email.data):
            flash("Usuario y/o contraseña invalidos","error")
            return redirect(url_for("acceso.login"))

        if not buscar_usuario_por_email(form.email.data).password:
            flash("Necesita terminar de registrarse, revise su correo electrónico.")
            return redirect(url_for("acceso.login"))

        user = autenticacion.chequear_usuario(form.email.data, form.password.data)

        if not user:
            flash("Usuario y/o contraseña invalidos", "error")
            return redirect(url_for("acceso.login"))

        if not esta_activo(user.email):
            flash("Fuiste deshabilitado por el administrador.", "error")
            return redirect(url_for("acceso.login"))

        session["usuario"] = user.email

        flash("La sesión se inició correctamente", "success")
        return redirect(url_for("home"))

    return render_template("autenticacion/login.html", form=form)


@acceso_bp.get("/logout")
def logout():
    """
    Cierra la sesión del usuario autenticado
    """
    if session["usuario"]:
        del session["usuario"]
        session.clear()
        flash("La sesión se cerró correctamente", "info")
        if "google_token" in session:
            session.pop("google_token", None)
    else:
        flash("No estás logueado", "info")

    return redirect(url_for("acceso.login"))


@acceso_bp.get("/quiensoy")
@necesita_login()
def quiensoy():
    return "soy " + session["usuario"]
