from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import session

from src.core.usuarios_institucion.formularios import CreateForm
from src.web.helpers.autenticacion import necesita_login
from src.core.usuarios_institucion import (
    agregar_user_rol_institucion,
    get_usuarios_institucion,
    delete_rol,
    update_user_rol_institucion,
    get_usuario,
    get_usuarios_institucion_paginated,
)
from src.core.autenticacion import buscar_usuario_por_email
from src.core import configuracion

usuarios_institucion_bp = Blueprint(
    "usuarios-institucion", __name__, url_prefix="/usuarios-institucion"
)

"""
Dueño/a: index, create, destroy, update.
"""


@usuarios_institucion_bp.route("/", methods=["GET"], defaults={"page": 1})
@usuarios_institucion_bp.route("/<int:page>", methods=["GET"])
@necesita_login(["userinst_index"])
def index(page):
    """
    Vista principal.
    Muestra index.html.
    Envía los usuarios y sus roles de forma paginada.
    """

    usuario = buscar_usuario_por_email(session["usuario"])
    institucion = usuario.institucion_activa_id
    page = page
    per_page = configuracion.get_cant_elementos_pag()
    usuarios = get_usuarios_institucion_paginated(
        institucion, page=page, per_page=per_page
    )

    return render_template(
        "usuarios_institucion/index.html", usuarios=usuarios, usuario=usuario
    )


@necesita_login(["userinst_create"])
@usuarios_institucion_bp.route("/create", methods=["GET", "POST"])
def create():
    """
    Vista de asignación de un rol a un email.
    Muestra create.html.
    Envía el formulario.
    Evalua si el usuario existe o si ya tiene un rol.
    """

    form = CreateForm()
    if form.validate_on_submit():
        email = request.form["email"]
        rol = request.form["rol"].lower()
        institucion = buscar_usuario_por_email(session["usuario"]).institucion_activa_id

        if not buscar_usuario_por_email(email):
            flash("Este email no está registrado en el sistema.", "error")
            return redirect(url_for("usuarios-institucion.index"))

        if get_usuario(email, rol, institucion):
            flash("Este usuario ya tiene un rol asignado a esta institución.", "error")
            return redirect(url_for("usuarios-institucion.index"))

        agregar_user_rol_institucion(email, rol, institucion)
        flash("Se agregó el rol al usuario.", "success")
        return redirect(url_for("usuarios-institucion.index"))
    elif not form.validate_on_submit() and request.method == "POST":
        flash("Ocurrió un error.", "error")

    return render_template("usuarios_institucion/create.html", form=form)


@necesita_login(["userinst_destroy"])
@usuarios_institucion_bp.get("/destroy/<email>")
def destroy(email):
    """
    Controlador para eliminar la institución.
    """
    if email:
        institucion = buscar_usuario_por_email(session["usuario"]).institucion_activa_id
        delete_rol(email, institucion)
        flash("Se eliminó el rol para el usuario exitosamente.", "success")
        return redirect(url_for("usuarios-institucion.index"))


@usuarios_institucion_bp.route("/update/<email>/<rol>", methods=["GET", "POST"])
@necesita_login(["userinst_update"])
def update(email=None, rol=None):
    """
    Vista de actualización de un rol a un email.
    Muestra update.html.
    Envía el formulario.
    """
    institucion = buscar_usuario_por_email(session["usuario"]).institucion_activa_id
    usuario_rol = {"email": email, "rol": rol}

    form = CreateForm()
    if form.validate_on_submit():
        rol = request.form["rol"].lower()
        update_user_rol_institucion(email, rol, institucion)
        flash("Se actualizó el rol al usuario exitosamente.", "success")
        return redirect(url_for("usuarios-institucion.index"))
    elif not form.validate_on_submit() and request.method == "POST":
        flash("Ocurrió un error.", "error")

    return render_template(
        "usuarios_institucion/update.html", form=form, usuario=usuario_rol
    )
