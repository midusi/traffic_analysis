from src.core.database import db

from src.core.institucion.models.institucion import Institucion


def list_instituciones():
    """
    Lista todas las instituciones ordenadas por nombre.
    """

    instituciones = Institucion.query.order_by(Institucion.nombre).all()

    return instituciones


def list_instituciones_paginated(page, per_page):
    """
    Lista todas las instituciones ordenadas por nombre y paginadas segun per_page.
    Utiliza page y per_page para paginar.
    """

    instituciones = Institucion.query.order_by(Institucion.nombre).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return instituciones


def create_institucion(**kwargs):
    """
    Crea una institución.
    """

    institucion = Institucion(**kwargs)
    db.session.add(institucion)
    db.session.commit()

    return institucion


def update_institucion(**kwargs):
    """
    Actualiza la institución.
    """

    institucion = get_institucion_by_id(kwargs["id"])
    institucion.nombre = kwargs["nombre"]
    institucion.info = kwargs["info"]
    institucion.direccion = kwargs["direccion"]
    institucion.localizacion = kwargs["localizacion"]
    institucion.web = kwargs["web"]
    institucion.palabra_clave = kwargs["palabra_clave"]
    institucion.horario_atencion = kwargs["horario_atencion"]
    institucion.email = kwargs["email"]
    institucion.telefono = kwargs["telefono"]

    db.session.commit()


def delete_institucion(id):
    """
    Elimina la institución.
    """
    if get_institucion_by_id(id):
        Institucion.query.filter_by(id=id).delete()
    db.session.commit()


def get_institucion_by_id(id):
    """
    Obtiene una institución dado un id.
    """
    institucion = Institucion.query.get(id)

    return institucion


def get_institucion_by_name(nombre):
    """
    Obtiene una institución dado un nombre.
    """

    institucion = Institucion.query.filter_by(nombre=nombre).first()

    return institucion


def activate_institucion(id):
    """
    Activa una institución.
    """

    institucion = get_institucion_by_id(id)
    institucion.habilitado = True
    db.session.commit()


def deactivate_institucion(id):
    """
    Desactiva una institución.
    """

    institucion = get_institucion_by_id(id)
    institucion.habilitado = False
    db.session.commit()
