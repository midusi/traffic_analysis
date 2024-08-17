from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy.exc import IntegrityError

from src.core.database import db

from src.core.institucion.models.institucion import Institucion
from src.core.institucion.formularios import CreateForm
from src.web.helpers.autenticacion import necesita_login

from src.core import configuracion
from src.core import institucion

instituciones_bp = Blueprint("instituciones", __name__, url_prefix="/instituciones")

"""
Permisos:

Super Administrador/a: index, show, update, create, destroy, activate, deactivate.
"""


@instituciones_bp.route("/", methods=["GET"], defaults={"page": 1})
@instituciones_bp.route("/<int:page>", methods=["GET"])
@necesita_login(["institucion_index"])
def index(page):
    """
    Vista principal.
    Muestra index.html.
    Envía las instituciones paginadas.
    """

    page = page
    per_page = configuracion.get_cant_elementos_pag()
    instituciones = institucion.list_instituciones_paginated(
        page=page, per_page=per_page
    )

    return render_template(
        "instituciones/index.html",
        instituciones=instituciones,
    )


@instituciones_bp.get("/show/<id>")
@necesita_login(["institucion_show"])
def show(id):
    """
    Vista individual de la institución.
    Muestra show.html.
    Envía la institución consultada.
    """

    inst = institucion.get_institucion_by_id(id)

    return render_template("instituciones/show.html", institucion=inst)


@instituciones_bp.route("/update/<id>", methods=["GET", "POST"])
@necesita_login(["institucion_update"])
def update(id):
    """
    Vista de actualización de una institución.
    Muestra update.html.
    Envía las institucion a modificar y el formulario.
    """

    inst = institucion.get_institucion_by_id(id)
    form = CreateForm()
    if form.validate_on_submit():
        nombre = request.form["nombre"]

        institucion_repetida = institucion.get_institucion_by_name(nombre)
        if institucion_repetida and (int(institucion_repetida.id) != int(id)):
            flash("Ya existe una institucion con este nombre.", "error")
            return redirect(url_for("instituciones.index"))

        informacion = request.form["info"]
        direccion = request.form["direccion"]
        localizacion = request.form["localizacion"]
        web = request.form["web"]
        palabra_clave = request.form["palabra_clave"].split(",")
        horario_atencion = request.form["horario_atencion"]
        email = request.form["email"]
        telefono = request.form["telefono"]

        institucion.update_institucion(
            id=id,
            nombre=nombre,
            info=informacion,
            direccion=direccion,
            localizacion=localizacion,
            web=web,
            palabra_clave=palabra_clave,
            horario_atencion=horario_atencion,
            email=email,
            telefono=telefono,
        )
        flash("Se actualizó la institución exitosamente.", "success")
        return redirect(url_for("instituciones.index"))
    elif not form.validate_on_submit() and request.method == "POST":
        flash("Ocurrió un error.", "error")
    return render_template("instituciones/update.html", institucion=inst, form=form)


@necesita_login(["institucion_create"])
@instituciones_bp.route("/create", methods=["GET", "POST"])
def create():
    """
    Vista de creación de una institución.
    Muestra create.html.
    Envía el formulario.
    """

    form = CreateForm()
    if form.validate_on_submit():
        nombre = request.form["nombre"]

        institucion_repetida = institucion.get_institucion_by_name(nombre)
        if institucion_repetida:
            flash("Ya existe una institucion con este nombre.", "error")
            return redirect(url_for("instituciones.index"))

        informacion = request.form["info"]
        direccion = request.form["direccion"]
        localizacion = request.form["localizacion"]
        web = request.form["web"]
        palabra_clave = request.form["palabra_clave"].split(",")
        horario_atencion = request.form["horario_atencion"]
        email = request.form["email"]
        telefono = request.form["telefono"]

        institucion.create_institucion(
            nombre=nombre,
            info=informacion,
            direccion=direccion,
            localizacion=localizacion,
            web=web,
            palabra_clave=palabra_clave,
            horario_atencion=horario_atencion,
            email=email,
            telefono=telefono,
        )

        flash("Se agregó la institución exitosamente.", "success")
        return redirect(url_for("instituciones.index"))
    elif not form.validate_on_submit() and request.method == "POST":
        flash("Ocurrió un error.", "error")

    return render_template("instituciones/create.html", form=form)


@necesita_login(["institucion_destroy"])
@instituciones_bp.post("/delete/<id>")
def destroy(id=None):
    """
    Controlador para eliminar la institución.
    """

    if id:
        try:
            institucion.delete_institucion(id)
            flash("Se eliminó la institución exitosamente.", "success")
            return redirect(url_for("instituciones.index"))
        except IntegrityError:
            flash(
                "No se puede eliminar la institución debido a hay usuarios perteneciente a la misma.",
                "error",
            )
            return redirect(url_for("instituciones.index"))


@necesita_login(["institucion_activate"])
@instituciones_bp.get("/activate/<id>")
def activate(id):
    """
    Controlador para activar la institución.
    """

    institucion.activate_institucion(id)
    flash("Se activó la institución exitosamente.", "success")
    return redirect(url_for("instituciones.show", id=id))


@necesita_login(["institucion_deactivate"])
@instituciones_bp.get("/deactivate/<id>")
def deactivate(id):
    """
    Controlador para desactivar la institución.
    """

    institucion.deactivate_institucion(id)
    flash("Se desactivó la institución exitosamente.", "success")
    return redirect(url_for("instituciones.show", id=id))
