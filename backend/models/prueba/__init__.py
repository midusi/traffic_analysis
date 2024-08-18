from backend.models.prueba.prueba import Prueba
from backend.models.database import db

def create_prueba(**kwargs):
    prueba = Prueba(**kwargs)
    db.session.add(prueba)
    db.session.commit()
    return prueba


def list_pruebas():
    return Prueba.query.all()