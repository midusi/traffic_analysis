from datetime import datetime
from src.core.database import db
from sqlalchemy import Enum

publicado_por_enum = Enum('Cliente', 'Institución', name='publicado_por')

class Anotaciones(db.Model):
    __tablename__ = "anotaciones"
    id = db.Column(db.Integer, primary_key=True, unique=True)

    solicitud_id = db.Column(db.Integer, db.ForeignKey('solicitud.id', ondelete='CASCADE'))
    contenido = db.Column(db.String, nullable=False)
    publicado_por = db.Column(publicado_por_enum, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __init__(self, solicitud_id=None, contenido=None, publicado_por=None, fecha=None):
        self.solicitud_id = solicitud_id
        self.contenido = contenido
        self.publicado_por = publicado_por
        self.fecha = fecha