from src.web.helpers.autenticacion import necesita_login, necesita_institucion_activa
from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import session
from src.core.servicio.formularios import CreateForm
from src.core import autenticacion
# Cambio de nombre porque no me lo tomaba
from src.core import servicio as Servicio
from flask_paginate import Pagination, get_page_parameter


servicios_bp = Blueprint("servicios", __name__, url_prefix="/servicios")


@servicios_bp.get("/")
@servicios_bp.route("/", methods=["GET"])
@necesita_login(["servicio_index"])
@necesita_institucion_activa
def index():
    """Controlador para la vista paginada de los servicios de una institucion, brinda la posibilidad de aplicar filtros"""
    if request.args.get("page"):
        page = int(request.args.get("page"))
    else:
        page = 1

    per_page = 1
    # per_page = configuracion.get_cant_elementos_pag()
    q = request.args.get("q")  # palabra clave, criterio primario de busqueda
    tipo = request.args.get("tipo")  # busqueda secundaria
    usuario = autenticacion.buscar_usuario_por_email(session["usuario"])
    inst = usuario.institucion_activa_id
    servicios = Servicio.listar_servicios_paginated_by_institucion(
        page=page, per_page=per_page, palabra_clave=q, tipo=tipo, institucion_id=inst
    )
    return render_template(
        "servicios/index.html", servicios=servicios, q=q, tipo=tipo
    )


@servicios_bp.route("/create", methods=["GET", "POST"])
@necesita_login(["servicio_create"])
@necesita_institucion_activa
def create():
    """Controlador para crear un servicio, el cual sera asignado a la institucion activa de su creador"""
    form = CreateForm()
    form.tipo.choices = [(str(tipo.id), tipo.nombre)
                         for tipo in Servicio.list_tipos()]
    if form.validate_on_submit():
        usuario = autenticacion.buscar_usuario_por_email(session["usuario"])
        if usuario:
            inst = usuario.institucion_activa
            print(inst)
            for servicio in inst.servicios:
                if (servicio.nombre == request.form["nombre"]):
                    flash(
                        "Error: esta institucion ya tiene un servicio con ese nombre.")
                    return render_template("servicios/create.html", form=form)

        nombre = request.form["nombre"]
        descripcion = request.form["descripcion"]
        palabras_claves = request.form["palabras_claves"].split(",")
        tipo_id = request.form["tipo"]
        habilitado = True if "habilitado" in request.form else False
        Servicio.create_servicio(
            nombre=nombre,
            descripcion=descripcion,
            palabras_claves=palabras_claves,
            habilitado=habilitado,
            tipo_id=int(tipo_id),
            institucion_id=inst.id
        )
        flash("Servicio creado exitosamente.", "success")
        return (redirect(url_for("servicios.index")))
    elif not form.validate_on_submit() and request.method == "POST":
        flash("ocurrio un error.", "error")
    return render_template("servicios/create.html", form=form)


@servicios_bp.route("/update/<id>", methods=["GET", "POST"])
@necesita_login(["servicio_update"])
@necesita_institucion_activa
def update(id):
    """Controlador para actualizar un servicio"""
    servicio = Servicio.get_servicio_by_id(id)
    form = CreateForm()

    form.tipo.choices = [(str(tipo.id), tipo.nombre)
                         for tipo in Servicio.list_tipos()]

    # sin esta linea el valor de tipo se setea siempre en el primer tipo de la linea,indiferentemente del valor que en realidad tiene
    form.tipo.data = str(servicio.tipo_id)

    if form.validate_on_submit():
        usuario = autenticacion.buscar_usuario_por_email(session["usuario"])
        if usuario:
            inst = usuario.institucion_activa
            for s in inst.servicios:
                if s.nombre == request.form["nombre"] and s.id != int(id):
                    flash(
                        "Error: esta institución ya tiene un servicio con ese nombre.")
                    return render_template("servicios/update.html", servicio=servicio, form=form)

            nombre = request.form["nombre"]
            descripcion = request.form["descripcion"]
            palabras_claves = request.form["palabras_claves"].split(",")
            tipo_id = request.form["tipo"]
            Servicio.update_servicio(
                id=id,
                nombre=nombre,
                descripcion=descripcion,
                palabras_claves=palabras_claves,
                tipo=tipo_id
            )
            flash("Servicio actualizado exitosamente.", "success")
            return redirect(url_for("servicios.index"))
        elif not form.validate_on_submit() and request.method == "POST":
            flash("Ocurrió un error.", "error")
    return render_template("servicios/update.html", servicio=servicio, form=form)


@servicios_bp.get("/activate/<id>")
@necesita_login(["servicio_update"])
@necesita_institucion_activa
def activate(id):
    """Controlador para activar un servicio"""
    Servicio.activate_servicio(id)
    flash("Servicio habilitado exitosamente.", "success")
    return redirect(url_for("servicios.show", id=id))


@servicios_bp.get("/deactivate/<id>")
@necesita_login(["servicio_update"])
@necesita_institucion_activa
def deactivate(id):
    """Controlador para desactivar un servicio"""
    Servicio.deactivate_servicio(id)
    flash("Servicio deshabilitado exitosamente.", "success")
    return redirect(url_for("servicios.show", id=id))


@servicios_bp.get("/show/<id>")
@necesita_login(["servicio_show"])
def show(id):
    """Controlador para mostrar un servicio de manera individual"""
    serv = Servicio.get_servicio_by_id(id)

    return render_template("servicios/show.html", servicio=serv)


@servicios_bp.post("/delete/<id>")
@necesita_login(["servicio_destroy"])
@necesita_institucion_activa
def destroy(id=None):
    """Controlador para eliminar una institucion"""
    if id:
        Servicio.delete_servicio(id)
        flash("Servicio eliminado exitosamente.", "success")
        return redirect(url_for("servicios.index"))

