import datetime

from src.core.database import db
from src.core.solicitudes.models.estado_cambios import EstadoCambios

class Solicitud(db.Model):
    __tablename__ = "solicitud"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    fecha_creacion = db.Column(db.Date, nullable=False)
    detalle = db.Column(db.String, nullable=True)
    archivo_adjunto = db.Column(db.String, nullable=True)

    servicio_id = db.Column(db.Integer, db.ForeignKey("servicio.id"))
    servicio = db.relationship('Servicio', foreign_keys=[servicio_id])
    
    estado_id = db.Column(db.Integer, db.ForeignKey("estado_solicitud.id"))
    estado_actual = db.relationship('EstadoSolicitud', foreign_keys=[estado_id])
    cambios_estado = db.relationship('EstadoCambios')
    anotaciones = db.relationship('Anotaciones')

    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    usuario = db.relationship('Usuario', foreign_keys=[usuario_id])
    
    def __init__(self, detalle=None, archivo_adjunto=None, servicio_id=None, usuario_id=None,nombre_servicio=None):
        EstadoCambios(comentario="Creacion de la solicitud", estado_id=1, solicitud_id=self.id)
        self.fecha_creacion = datetime.datetime.now()
        self.estado_id = 1
        self.detalle = detalle
        self.archivo_adjunto = archivo_adjunto
        self.servicio_id = servicio_id
        self.usuario_id = usuario_id
        self.nombre_servicio=nombre_servicio
