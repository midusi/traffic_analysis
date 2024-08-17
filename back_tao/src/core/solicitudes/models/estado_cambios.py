import datetime
from src.core.database import db

class EstadoCambios(db.Model):
    __tablename__ = "estado_cambios"
    
    id = db.Column(db.Integer, primary_key=True, unique=True)

    solicitud_id = db.Column(db.Integer, db.ForeignKey('solicitud.id', ondelete='CASCADE'))
    estado_id = db.Column(db.Integer, db.ForeignKey('estado_solicitud.id'))
    estado = db.Relationship('EstadoSolicitud', foreign_keys=[estado_id])

    fecha = db.Column(db.DateTime, nullable=False)
    comentario = db.Column(db.String, nullable=False)

    def __init__(self, solicitud_id=None, estado_id=None, comentario=None):
        self.solicitud_id=solicitud_id
        self.estado_id=estado_id
        self.comentario=comentario
        self.fecha=datetime.datetime.now()