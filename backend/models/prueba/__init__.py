from backend.models.prueba.prueba import Prueba
from backend.models.database import db

def create_prueba(**kwargs):
    prueba = Prueba(**kwargs)
    db.session.add(prueba)
    db.session.commit()
    return prueba


def list_pruebas(page, per_page):
    return Prueba.query.paginate(page=page, per_page=per_page, error_out=True)