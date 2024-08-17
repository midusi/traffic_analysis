from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for, session
from flask_paginate import Pagination, get_page_parameter
from src.core.autenticacion.formularios import CreateForm, UpdateForm, AgregarInstitucionForm
# dentro de autenticacion esta definido usuario
from src.core import autenticacion

# from src.core import configuracion
from src.core import institucion as inst
from src.core import usuarios_institucion
from src.web.helpers.autenticacion import necesita_login
from src.core import configuracion

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


@usuarios_bp.route("/", methods=["GET"])
@necesita_login(["user_index"])
def index():
    """Vista paginada del index, muestra todos los usuarios, con posibilidad de aplicar filtros"""
    if request.args.get("page"):
        page = int(request.args.get("page"))
    else:
        page = 1

    per_page = configuracion.get_cant_elementos_pag()
    email = request.args.get("email")
    activo = request.args.get("activo")

    usuarios = autenticacion.listar_usuarios_paginated(
        page=page, per_page=per_page, email=email, activo=activo
    )
    return render_template(
        "usuarios/index.html", usuarios=usuarios, activo=activo, email=email
    )


@usuarios_bp.get("/show/<id>")
@necesita_login(["user_show"])
def show(id):
    """Vista individual de un usuario."""
    usuario = autenticacion.buscar_usuario_por_id(id)

    return render_template("usuarios/show.html", usuario=usuario)


@usuarios_bp.route("/update/<id>", methods=["GET", "POST"])
@necesita_login(["user_update"])
def update(id):
    """Controlador para actualizar un usuario"""
    usuario = autenticacion.buscar_usuario_por_id(id)
    form = UpdateForm()
    if form.validate_on_submit():
        # Verifico si el username ya esta registrado
        existing_user = autenticacion.buscar_usuario_por_username(
            request.form["username"]
        )
        if existing_user and existing_user.id != int(id):
            flash("Error: El nombre de usuario ya está registrado.", "error")
            return render_template("usuarios/update.html", usuario=usuario, form=form)

        # Verifico si el correo ya esta registrado
        existing_user = autenticacion.buscar_usuario_por_email(
            request.form["email"])
        if existing_user and existing_user.id != int(id):
            flash("Error: El correo electrónico ya está registrado.", "error")
            return render_template("usuarios/update.html", usuario=usuario, form=form)
        username = request.form["username"]
        email = request.form["email"]
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        autenticacion.update_usuario(
            id=id,
            username=username,
            email=email,
            nombre=nombre,
            apellido=apellido,
        )
        flash("Usuario actualizado exitosamente.", "success")
        return redirect(url_for("usuarios.index"))
    elif not form.validate_on_submit() and request.method == "POST":
        flash("Ocurrió un error.", "error")
    return render_template("usuarios/update.html", usuario=usuario, form=form)


@usuarios_bp.route("/create", methods=["GET", "POST"])
@necesita_login(["user_create"])
def create():
    """Controlador para crear un usuario"""
    form = CreateForm()
    # Cargo opciones para los campos rol e institucion directamente en el formulario
    choices = [(str(insti.nombre), insti.nombre)
               for insti in inst.list_instituciones()]
    choices.insert(0, ("no_tiene", "No tiene"))
    form.institucion.choices = choices

    if form.validate_on_submit():
        # Verifico si el username ya esta registrado
        existing_user = autenticacion.buscar_usuario_por_username(
            request.form["username"]
        )
        if existing_user:
            flash("Error: El nombre de usuario ya está registrado.", "error")
            return render_template("usuarios/create.html", form=form)

        # Verifico si el correo ya esta registrado
        existing_user = autenticacion.buscar_usuario_por_email(
            request.form["email"])
        if existing_user:
            flash("Error: El correo electrónico ya está registrado.", "error")
            return render_template("usuarios/create.html", form=form)

        rolAux = request.form["rol"]
        instiAux = request.form["institucion"]
        if not rolAux or not instiAux:
            flash("Error: Debes seleccionar un rol e institución válidos.", "error")
            return render_template("usuarios/create.html", form=form)

        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        rol = request.form["rol"].lower()
        institucion = instiAux
        autenticacion.crear_usuario(
            username=username,
            password=password,
            email=email,
            nombre=nombre,
            apellido=apellido,
            rol=rol,
            institucion=institucion,
        )
        flash("Usuario creado exitosamente.", "success")
        return redirect(url_for("usuarios.index"))

    elif not form.validate_on_submit() and request.method == "POST":
        flash("Ocurrió un error.", "error")
    return render_template("usuarios/create.html", form=form)


@usuarios_bp.route("/agregar-institucion/<id>", methods=["GET", "POST"])
@necesita_login(["user_update"])
def agregar_institucion(id):
    """Controlador para agregar una institucion a un usuario"""
    form = AgregarInstitucionForm()
    choices = [(str(insti.nombre), insti.nombre)
               for insti in inst.list_instituciones()]
    form.institucion.choices = choices

    if form.validate_on_submit():
        institucion_id = inst.get_institucion_by_name(
            request.form["institucion"]).id
        insti_aux = inst.get_institucion_by_id(institucion_id)
        usuario = autenticacion.buscar_usuario_por_id(id)
        rol = request.form["rol"].lower()
        if insti_aux in autenticacion.get_instituciones_by_id(id):
            flash("El usuario ya tiene asignada esta institucion.")
            return redirect(url_for("usuarios.agregar_institucion" , id=id))
        print(rol)
        usuarios_institucion.agregar_user_rol_institucion(
            usuario.email, rol, institucion_id)
        flash("Institucion asignada exitosamente.", "success")
        return redirect(url_for("usuarios.index"))
    elif not form.validate_on_submit() and request.method == "POST":
        flash("Ocurrio un error.", "error")
    return render_template("/usuarios/agregar-institucion.html", form=form, id=id)


@usuarios_bp.post("/delete/<id>")
@necesita_login(["user_destroy"])
def destroy(id=None):
    """Controlador para eliminar un usuario"""
    if id:
        autenticacion.delete_usuario(id)
        flash("Usuario eliminado exitosamente.", "success")
        return redirect(url_for("usuarios.index"))


@usuarios_bp.get("/activate/<id>")
@necesita_login(["user_activate"])
def activate_usuario(id):
    """Controlador para activar un usuario"""
    autenticacion.activate_usuario(id)
    flash("Usuario habilitado exitosamente.", "success")
    return redirect(url_for("usuarios.show", id=id))


@usuarios_bp.get("/deactivate/<id>")
@necesita_login(["user_deactivate"])
def deactivate_usuario(id):
    """Controlador para desactivar un usuario"""
    autenticacion.deactivate_usuario(id)
    flash("Usuario deshabilitado exitosamente.", "success")
    return redirect(url_for("usuarios.show", id=id))


@usuarios_bp.route("/mis-instituciones/<id>")
@necesita_login(["user_instituciones"])
def mostrar_instituciones(id):
    """Controlador para mostrar las instituciones a las que pertenece un usuario, incluyendo la institucion activa"""
    user = autenticacion.buscar_usuario_por_id(id)
    if user is not None:
        # Recupera las instituciones del usuario
        instituciones = autenticacion.get_instituciones_by_id(id)

        return render_template(
            "usuarios/instituciones-del-usuario.html",
            usuario=user,
            instituciones=instituciones,
        )
    else:
        flash("Usuario no encontrado", "error")
        return redirect(url_for("usuarios.index"))


@usuarios_bp.route("/activar-institucion/<int:institution_id>")
def activar_institucion(institution_id):
    """Controlador para asignar una institucion activa"""
    user = autenticacion.buscar_usuario_por_email(session["usuario"])
    if user is not None:
        autenticacion.asignar_institucion_activa(user.id, institution_id)
        flash("Institución activa asignada con éxito", "success")
        return redirect("/mis-instituciones")
    else:
        flash("Fallo la activación", "error")
        return redirect("/mis-instituciones")
