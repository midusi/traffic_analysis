from datetime import datetime

from src.core.institucion.models.institucion import Institucion
from src.core.solicitudes.models.estado_cambios import EstadoCambios
from src.core.solicitudes.models.anotaciones import Anotaciones
from src.core.servicio.models.servicio import Servicio
from src.core.solicitudes.models.estado_solicitud import EstadoSolicitud
from src.core.solicitudes.models.solicitud import Solicitud
from src.core.database import db
from sqlalchemy import func

from sqlalchemy import asc, desc

def create_solicitud(**kwargs):
    """ crea una nueva solicitud """
    solicitud = Solicitud(**kwargs)
    db.session.add(solicitud)
    db.session.commit()

    return solicitud

def get_solicitudes():
    """ retorna un listado con todas las solicitudes """
    solicitudes = Solicitud.query.all()
    return solicitudes

def set_archivo_adjunto(id,archivo):
    solicitud=find_solicitud_id(id)
    solicitud.archivo_adjunto=archivo
    db.session.commit()
    return solicitud


def get_solicitudes_paginated(page, per_page):
    solicitudes = Solicitud.query.paginate(page=page, per_page=per_page, error_out=False)
    return solicitudes

def get_solicitudes_by_user_paginated(usuario_id, page, per_page, sort, order):

    if order not in ['asc', 'desc']:
        raise ValueError(f'El valor del campo "order" es inválido. Debe ser "asc" o "desc" (se recibió "{order}")')
    if sort not in ['id', 'fecha_creacion', 'estado_id', 'servicio_id', 'detalle']:
        raise ValueError(f'El valor del campo "sort" no es válido para ordenar las solicitudes (se recibió "{sort}")')

    solicitudes_query = Solicitud.query.filter_by(usuario_id=usuario_id)

    try:
        if order == 'asc':
            solicitudes_query = solicitudes_query.order_by(asc(getattr(Solicitud, sort)))
        elif order == 'desc':
            solicitudes_query = solicitudes_query.order_by(desc(getattr(Solicitud, sort)))
    except AttributeError:
        raise ValueError(f'El valor del campo "sort" no es válido para ordenar las solicitudes (se recibió "{sort}")')

    solicitudes = solicitudes_query.paginate(page=page, per_page=per_page, error_out=False)
    
    return solicitudes

def find_solicitud_id(id):
    """ encuentra una solicitud por su ID"""
    solicitud = Solicitud.query.filter_by(id=id).first()

    solicitud.anotaciones = sorted(solicitud.anotaciones, key=lambda x:x.fecha, reverse=True)
    return solicitud

def find_solicitudes_servicio(servicio_id):
    """encuentra todas las solicitudes correspondientes a un servicio"""
    solicitudes = Solicitud.query.filter_by(servicio_id=servicio_id).all()
    return solicitudes

def update_solicitud(**kwargs):
    """actualiza el estado y las anotaciones de una solicitud"""
    solicitud = find_solicitud_id(kwargs["id"])
    solicitud.estado_id = kwargs["estado_id"] or solicitud.estado_id

    db.session.commit()
    return solicitud

def delete_solicitud(id):
    if find_solicitud_id(id):
        Solicitud.query.filter_by(id=id).delete()
    db.session.commit()

def create_estado(**kwargs):
    """crea un estado de solicitud"""
    estado = EstadoSolicitud(**kwargs)
    db.session.add(estado)
    db.session.commit()

    return estado

def get_estados():
    """obtiene un listado con todos los estados"""
    estados = EstadoSolicitud.query.all()
    return estados

def find_estado_id(id):
    """obtiene un estado por su ID"""
    estado = EstadoSolicitud.query.filter_by(id=id).first()
    return estado

def find_solicitud_by_servicio(servicio_id):
    """busca las solicitudes realizadas a un servicio en particular"""
    solicitudes = Solicitud.query.filter_by(servicio_id=servicio_id).all()
    return solicitudes

def find_solicitud_by_estado(estado_id):
    """busca las solicitudes que se encuentren en un estado en particular"""
    solicitudes = Solicitud.query.filter_by(estado_id=estado_id).all()
    return solicitudes

def find_solicitud_by_institucion(institucion_id):
    """busca las solicitudes correspondientes a servicios de una institucion"""
    solicitudes = Solicitud.query.join(Servicio, Solicitud.servicio_id==Servicio.id).filter_by(institucion_id=institucion_id)
    return solicitudes

def find_solicitud_by_institucion_filter(institucion_id, page, per_page, tipo_id=None, estado_id=None, fecha_inicio=None, fecha_fin=None,cliente=None):
    """busca las solicitudes correspondientes a servicios de una institución, realizando el filtrado y paginado"""
    solicitudes = Solicitud.query.join(Servicio, Solicitud.servicio_id==Servicio.id).filter(Servicio.institucion_id == institucion_id)

    if tipo_id:
        solicitudes = solicitudes.filter(Servicio.tipo_id == tipo_id)
    if estado_id:
        solicitudes = solicitudes.filter(Solicitud.estado_id == estado_id)
    if fecha_inicio:
        solicitudes = solicitudes.filter(Solicitud.fecha_creacion >= fecha_inicio)
    if fecha_fin:
        solicitudes = solicitudes.filter(Solicitud.fecha_creacion <= fecha_fin)
    if cliente:
        solicitudes = solicitudes.filter(Solicitud.cliente.has(Cliente.nombre.ilike(f"%{cliente}%")))

    solicitudes = solicitudes.order_by(Solicitud.fecha_creacion).paginate(page=page,per_page=per_page,error_out=False)
    return solicitudes

def find_estados_solicitud_by_id(solicitud_id):
    """busca los comentarios sobre el cambio de estado de una solicitud"""
    estados = EstadoCambios.query.filter_by(solicitud_id=solicitud_id).all()
    return estados

def create_estado_cambios(**kwargs):
    """crea un nuevo cambio de estado para una solicitud"""
    estado_cambios = EstadoCambios(**kwargs)
    db.session.add(estado_cambios)
    db.session.commit()

def create_anotaciones(**kwargs):
    """crea una anotación"""
    anotaciones = Anotaciones(**kwargs)
    db.session.add(anotaciones)
    db.session.commit()

def add_anotacion_to_solicitud(solicitud_id, contenido, publicado_por):
    """crea una anotación para la solicitud deseada
        - usar siempre este método en vez de create_anotaciones
        - publicado_por recibe el valor 'Cliente' si la solicitud se creó desde la API o 'Institución' si se creó desde la app privada"""
    create_anotaciones(solicitud_id=solicitud_id, contenido=contenido, publicado_por=publicado_por,fecha=datetime.now())

def count_solicitudes_by_estado():
    resultados = EstadoSolicitud.query.outerjoin(Solicitud, EstadoSolicitud.id == Solicitud.estado_id).with_entities(EstadoSolicitud.id, EstadoSolicitud.nombre, func.count(Solicitud.id).label('count')).group_by(EstadoSolicitud.id, EstadoSolicitud.nombre).order_by(EstadoSolicitud.id).all()
    return resultados

def get_servicios_mas_solicitados():
    resultados = Solicitud.query.join(Servicio).with_entities(Solicitud.servicio_id, Servicio.nombre, func.count().label('count')).group_by(Solicitud.servicio_id, Servicio.nombre).order_by(func.count().desc()).limit(5)
    return resultados

def count_solicitudes_by_institucion():
    resultados = Solicitud.query.join(Servicio).join(Institucion).with_entities(Servicio.institucion_id, Institucion.nombre, func.count().label('count')).group_by(Servicio.institucion_id, Institucion.nombre).limit(10)
    return resultados
