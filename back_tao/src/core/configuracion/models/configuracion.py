from src.core.database import db

class Configuracion(db.Model):
    __tablename__ = "configuracion"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    cant_elementos_pag = db.Column(db.Integer, nullable=False)
    mantenimiento = db.Column(db.Boolean, nullable=False)
    mantenimiento_msg = db.Column(db.String, nullable=False)

    def __init__(
        self,
        cant_elementos_pag=None,
        mantenimiento=None,
        mantenimiento_msg=None
    ):
        self.cant_elementos_pag = cant_elementos_pag
        self.mantenimiento = mantenimiento
        self.mantenimiento_msg = mantenimiento_msg