from src.core.database import db


class Tipo(db.Model):
    __tablename__ = "tipo"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String, nullable=False)


def __init__(self, nombre=None):
    self.nombre = nombre 
