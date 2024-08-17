from datetime import datetime
from src.core.servicio import list_tipos
from src.core.configuracion import get_cant_elementos_pag
from src.web.helpers.autenticacion import necesita_login, necesita_institucion_activa
from src.core.solicitudes import add_anotacion_to_solicitud, find_solicitud_by_institucion, find_solicitud_by_institucion_filter, update_solicitud, delete_solicitud, find_solicitud_id, find_estados_solicitud_by_id, get_estados, create_estado_cambios
from src.core.solicitudes.formularios import UpdateForm
import os
from src.core.autenticacion import buscar_usuario_por_email
from flask import Blueprint, render_template, session, redirect, url_for, flash, request,send_from_directory

solicitudes_bp = Blueprint("solicitudes", __name__, url_prefix="/solicitudes")


@solicitudes_bp.get("/")
@necesita_login(["solicitudes_index"])
def index():
    if request.args.get("page"):
        page = int(request.args.get("page"))
    else:
        page = 1
    
    tipo_id = int(request.args.get("tipo_id")) if request.args.get("tipo_id") else None
    estado_id = int(request.args.get("estado_id")) if request.args.get("estado_id") else None
    fecha_inicio = request.args.get("fecha_inicio")
    fecha_fin = request.args.get("fecha_fin")
    cliente = request.args.get("cliente")

    estados = get_estados()
    tipos_servicio = list_tipos()

    current_user = buscar_usuario_por_email(session["usuario"])
    solicitudes = find_solicitud_by_institucion_filter(current_user.institucion_activa_id,page,get_cant_elementos_pag(), tipo_id=tipo_id, estado_id=estado_id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, cliente=cliente)
    return render_template("solicitudes/index.html", solicitudes=solicitudes, estados=estados, tipos_servicio=tipos_servicio, tipo_id=tipo_id, estado_id=estado_id, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, cliente=cliente)

@solicitudes_bp.get("/<id>")
@necesita_login(["solicitudes_show"])
def show(id):
    estados = find_estados_solicitud_by_id(id)
    estados.sort(key=lambda x:x.fecha, reverse=True)

    return render_template("solicitudes/show.html", solicitud=find_solicitud_id(id))

@solicitudes_bp.route("/update/<int:id>", methods=["GET","POST"])
@necesita_login(["solicitudes_update"])
def update(id):
    solicitud = find_solicitud_id(id)
    form = UpdateForm(estado=solicitud.estado_id)
    form.estado.choices = [(str(x.id), x.nombre) for x in get_estados()]
    print(solicitud.estado_id)
    if form.validate_on_submit():
        estado = int(request.form["estado"])
        estado_comentario = request.form["comentario"]

        if (estado != solicitud.estado_id):
            create_estado_cambios(solicitud_id=solicitud.id,estado_id=estado,comentario=estado_comentario)

        update_solicitud(id=solicitud.id,estado_id=estado)
        
        flash("Solicitud actualizada con éxito", "success")
        return redirect(url_for("solicitudes.show", id=id))
    elif not form.validate_on_submit() and request.method == "POST":
        flash("Hubo un error al actualizar la solicitud", "error")

    print(solicitud.estado_id)
    return render_template("solicitudes/update.html", solicitud=solicitud, form=form)

@solicitudes_bp.post("/update/<int:id>/notes")
@necesita_login(["solicitudes_update"])
def add_anotacion(id):
    solicitud = find_solicitud_id(id)
    print(request.form)
    contenido = request.form["contenido"]
    if (not contenido or len(contenido) < 5):
        flash("El contenido de la anotación debe tener al menos 5 caracteres", "error")
        return redirect(url_for("solicitudes.show", id=id))
    
    add_anotacion_to_solicitud(id, contenido, "Institución")
    flash("Anotación agregada correctamente", "success")
    return redirect(url_for("solicitudes.show", id=id))

@solicitudes_bp.post("/destroy/<int:id>")
@necesita_login(["solicitudes_destroy"])
def destroy(id):
    try:
        delete_solicitud(id)
        flash("Se eliminó la solicitud con éxito", "success")
        return redirect(url_for("solicitudes.index"))
    except:
       flash("Hubo un error eliminando esta solicitud", "error")
       return redirect(url_for("solicitudes.show", id=id))
    
    
@solicitudes_bp.get('/uploads/<id>')
def download_file(id):
    if(id != None):
        try:
            ruta_carpeta_archivos = os.path.abspath('./files/'+str(id))
            archivo=os.listdir(ruta_carpeta_archivos)[0]
            print(archivo)
            print(ruta_carpeta_archivos)
            print(os.path.abspath(os.path.join(ruta_carpeta_archivos,archivo)))
            return send_from_directory(ruta_carpeta_archivos, archivo,as_attachment=True)
        except Exception as e:
            print(e)
            return e