from src.core.solicitudes.models.solicitud import Solicitud
from src.core.institucion.models.institucion import Institucion
from src.core.database import db
from src.core.servicio.models.servicio import Servicio
from src.core.servicio.models.tipo import Tipo
from sqlalchemy import String
from sqlalchemy import or_


def list_servicios():
    """Retorna una lista con todos los servicios del sistema"""
    servicios = Servicio.query.all()
    return servicios


def create_servicio(**kwargs):
    """Crea un servicio y lo retorna"""
    servicio = Servicio(**kwargs)
    db.session.add(servicio)
    db.session.commit()

    return servicio


def get_servicio_by_id(id):
    """Retorna un servicio dado su id"""
    servicio = Servicio.query.get(id)

    return servicio


def get_servicio_by_nombre(nombre):
    """Retorna un servicio dado su nombre"""
    servicio = Servicio.query.filter_by(nombre=nombre).first()
    return servicio


def get_tipo_by_id(id):
    """Retorna un tipo dado su id"""
    tipo = Tipo.query.get(id)

    return tipo


def list_servicios_by_institucion(id_institucion):
    """Retorna una lista con todos los servicios de una institucion dado su id"""
    servicios = Servicio.query.filter_by(institucion_id=id_institucion).all()
    return servicios


# TODO: chequear este metodo, ya que ahora los servicios no tienen centros habilitados
def actualizar_centros_habilitados(id, ids_instituciones):
    servicio = get_servicio_by_id(id)

    instituciones = Institucion.query.filter(
        Institucion.id.in_(ids_instituciones)
    ).all()

    for institucion in instituciones:
        servicio.instituciones.append(institucion)

    db.session.commit()


def activate_servicio(id):
    servicio = get_servicio_by_id(id)
    servicio.habilitado = True
    db.session.commit()


def deactivate_servicio(id):
    servicio = get_servicio_by_id(id)
    servicio.habilitado = False
    db.session.commit()


def create_tipo(**kwargs):
    tipo = Tipo(**kwargs)
    db.session.add(tipo)
    db.session.commit()

    return tipo


def update_servicio(**kwargs):
    servicio = get_servicio_by_id(kwargs["id"])
    servicio.nombre = kwargs["nombre"]
    servicio.descripcion = kwargs["descripcion"]
    servicio.palabras_claves = kwargs["palabras_claves"]
    servicio.tipo_id = kwargs["tipo"]

    db.session.commit()


def list_tipos():
    return Tipo.query.all()


def delete_servicio(id):
    Servicio.query.filter_by(id=id).delete()
    db.session.commit()


def listar_servicios_paginated(page, per_page, palabra_clave=None, tipo=None):
    servicios = Servicio.query

    if palabra_clave:
        servicios = servicios.filter(
            Servicio.palabras_claves.cast(String).ilike(f"%{palabra_clave}%")
        )

    if tipo:
        servicios = servicios.filter(Servicio.tipo.has(nombre=tipo))

    servicios = servicios.order_by(Servicio.nombre).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return servicios


def listar_servicios_habilitados_paginated(
    page, per_page, palabra_clave=None, tipo=None
):
    servicios = Servicio.query

    if palabra_clave:
        servicios = servicios.filter(
            or_(
                (Servicio.palabras_claves.cast(String).ilike(f"%{palabra_clave}%")),
                (Servicio.nombre.cast(String).ilike(f"%{palabra_clave}%")),
                (Servicio.descripcion.cast(String).ilike(f"%{palabra_clave}%")),
                (
                    Servicio.institucion_id.in_(
                        Institucion.query.filter(
                            Institucion.nombre.ilike(f"%{palabra_clave}%")
                        ).with_entities(Institucion.id)
                    )
                ),
            )
        )

    if tipo:
        servicios = servicios.filter(Servicio.tipo.has(nombre=tipo))

    servicios = servicios.filter(Servicio.habilitado == True)
    servicios = servicios.order_by(Servicio.nombre).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return servicios


def listar_servicios_paginated_by_institucion(
    page, per_page, palabra_clave=None, tipo=None, institucion_id=None
):
    servicios = Servicio.query.filter_by(institucion_id=institucion_id)

    if palabra_clave:
        servicios = servicios.filter(Servicio.palabras_claves.any(palabra_clave))

    if tipo:
        servicios = servicios.filter(Servicio.tipo.has(nombre=tipo))

    servicios = servicios.order_by(Servicio.nombre).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return servicios