from src.core.database import db

class InfoContacto(db.Model):
    __tablename__ = "info_contacto"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String, nullable=False, unique=False)
    activo = db.Column(db.Boolean, nullable=False)

    def __init__(
        self,
        nombre=None,
        activo=None
    ):
        self.nombre = nombre
        self.activo = activo