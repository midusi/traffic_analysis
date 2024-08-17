from src.core.database import db

from src.core.models.institucion import Institucion


def list_instituciones():
    instituciones = Institucion.query.all()

    return instituciones


def create_institucion(**kwargs):
    institucion = Institucion(**kwargs)
    db.session.add(institucion)
    db.session.commit()

    return institucion


def delete_institucion(id):
    Institucion.query.filter_by(id=id).delete()
    db.session.commit()
