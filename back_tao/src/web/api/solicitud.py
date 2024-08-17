from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from werkzeug.exceptions import UnsupportedMediaType
from flask import Flask, flash, request, redirect, url_for ,send_from_directory,Blueprint, current_app
from werkzeug.utils import secure_filename
import os 

UPLOAD_FOLDER = '../files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

from src.core.servicio import get_servicio_by_nombre
from src.core.solicitudes import (
    get_solicitudes_by_user_paginated,
    get_solicitudes_paginated,
    find_solicitud_id,
    create_solicitud,
    add_anotacion_to_solicitud,
    find_estado_id,
    set_archivo_adjunto
)
from src.core.configuracion import get_cant_elementos_pag
from src.web.schemas.solicitud import (
    solicitudes_schema,
    solicitudes_paginadas_schema,
    solicitud_schema,
    nueva_solicitud_schema,
    estado_schema,
    crear_anotacion_schema
)
from src.core.autenticacion import buscar_usuario_por_id

api_solicitudes_bp = Blueprint("solicitud_api", __name__, url_prefix="/api/me/requests")


@api_solicitudes_bp.get("/")
@jwt_required()
def get_solicitudes():
    """Devuelve las solicitudes de servicios pasandole en la url
    parametros opcionales:
    - page (default 1): página actual
    - per_page (default config): cantidad de elementos por página
    - sort (default fecha_creacion): campo por el que ordena elementos
    - order (default asc): orden ascendiente o descendiente"""
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=get_cant_elementos_pag(), type=int)
    sort = request.args.get("sort", default="fecha_creacion", type=str)
    order = request.args.get("order", "desc")

    try:
        solicitudes = get_solicitudes_by_user_paginated(get_jwt_identity(), page, per_page, sort, order)
    except ValueError as e:
        res = {
            'type': 'ValueError',
            'status': 'error',
            'message': str(e)
        }

        return jsonify(res), 400
    
    solicitudes_dumps = solicitudes_schema.dump(solicitudes)
    datos_serializados = solicitudes_paginadas_schema.dump(
        {
            "data": solicitudes_dumps,
            "page": page,
            "per_page": per_page,
            "total": solicitudes.total,
            "has_previous": solicitudes.has_prev,
            "has_next": solicitudes.has_next
        }
    )
    return datos_serializados


@api_solicitudes_bp.get("/<id>")
@jwt_required()
def get_solicitud_id(id):
    """Devuelve la solicitud realizada por el usuario autenticado."""

    solicitud = find_solicitud_id(id)
    if not solicitud:
        return {"error": "No existe o no se encontró un servicio con ese id."}, 400

    datos = solicitud_schema.dump(solicitud)
    return datos


@api_solicitudes_bp.post("/")
@jwt_required()
def cargar_solicitud():
    """Carga una solicitud de servicio por un usuario autenticado."""

    try:
        req_data = request.json
    except UnsupportedMediaType:
        return {
            "error": "Debe proveer el detalle en el contenido json de la peticion"
        }, 400

    try:
        data_validada = solicitud_schema.load(req_data)
    except ValidationError:
        return {"error": "Parametros invalidos"}, 400

    servicio_id = get_servicio_by_nombre(data_validada["nombre_servicio"]).id
    create_solicitud(detalle=data_validada["detalle"], servicio_id=servicio_id)

    return {"success": "Solicitud cargada con exito 😀"}


@api_solicitudes_bp.post("/<id>/notes")
@jwt_required()
def cargar_anotacion(id):
    """Carga una anotacion en una solicitud del usuario autenticado"""

    try:
        req_data = request.json
    except UnsupportedMediaType:
        return {
            "error": "Debe proveer el campo text en el contenido json de la peticion"
        }, 400

    try:
        data_validada = crear_anotacion_schema.load(req_data)
    except ValidationError:
        return {"error": "Parametros invalidos"}, 400

    solicitud = find_solicitud_id(id)
    if not solicitud:
        return {"error": "No existe o no se encontró una solicitud con ese id."}, 400

    usuario = buscar_usuario_por_id(
        solicitud.usuario_id
    )

    add_anotacion_to_solicitud(solicitud.id, data_validada["text"], "Cliente")

    return {"success": "Anotacion cargada con exito 😀"}

@api_solicitudes_bp.get("/estado/<id>")
@jwt_required()
def get_estado_id(id):
    """Devuelve la solicitud realizada por el usuario autenticado."""
    estado = find_estado_id(id)
    if not estado:
        return {"error": "No existe o no se encontró un estado con ese id."}, 400
    datos = estado_schema.dump(estado)
    return datos




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api_solicitudes_bp.post("/cargar/")
#@jwt_required()
def cargar_solicitud_2():
    print("Estás llegando al endpoint...")
    try:
        detalle = request.form.get('detalle')
        nombre_servicio = request.form.get('nombre_servicio')
        servicio_id = int(request.form.get('servicio_id'))
        archivo_adjunto = request.files.get('file') #En caso que no reciba nada sera None
        usuario_id = int(request.form.get('usuario_id'))
        print(usuario_id)

        solicitud_data = {
            'detalle': detalle,
            'nombre_servicio': nombre_servicio,
            'servicio_id': servicio_id,
            'usuario_id':usuario_id
        }
        solicitud_validada = nueva_solicitud_schema.load(solicitud_data)
        solicitud_creada=create_solicitud(
            detalle=solicitud_validada['detalle'],
            nombre_servicio=solicitud_validada['nombre_servicio'],
            servicio_id=solicitud_validada['servicio_id'],
            archivo_adjunto=None, #Esto para el download, xq necesitas el name
            usuario_id=solicitud_validada['usuario_id']
        )

        if archivo_adjunto and allowed_file(archivo_adjunto.filename):
            ruta_carpeta_archivos = './files/'+str(solicitud_creada.id)+"/"
            if not os.path.exists(ruta_carpeta_archivos):
                os.makedirs(ruta_carpeta_archivos)
            ruta_archivo = ruta_carpeta_archivos + archivo_adjunto.filename
            print(ruta_archivo)
            archivo_adjunto.save(ruta_archivo)
            print(ruta_archivo)
            alvaro845=set_archivo_adjunto(solicitud_creada.id,ruta_archivo)
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAA",alvaro845)
            #filename = secure_filename(archivo_adjunto.filename)
            #archivo_adjunto.save(os.path.join(current_app.config['UPLOAD_FOLDER'],filename))
    
            #Y con esto de arriba, ya se te guardo
        servicio_id = get_servicio_by_nombre(solicitud_validada["nombre_servicio"]).id
        if(archivo_adjunto):
            nombre_archivo = archivo_adjunto.filename
        else:
            nombre_archivo = None
        return {"success": "Solicitud y archivo cargados exitosamente 😀"}
    except ValidationError as ve:
        print(ve)
        return {"error": ve.messages}, 400
    except Exception as e:
        print(e)
        return {"error": str(e)}, 400