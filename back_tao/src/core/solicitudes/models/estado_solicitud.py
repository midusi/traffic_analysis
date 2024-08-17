from src.core.database import db

class EstadoSolicitud(db.Model):
    __tablename__ = "estado_solicitud"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String, nullable=False)

    def __init__(self, nombre=None):
        self.nombre = nombre