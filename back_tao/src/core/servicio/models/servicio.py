from src.core.database import db
from src.core.servicio.models import tipo


class Servicio(db.Model):
    __tablename__ = "servicio"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String, nullable=False, unique=True)
    descripcion = db.Column(db.String, nullable=False)
    palabras_claves = db.Column(db.ARRAY(db.String), nullable=False)
    # esta linea de abajo linkea con la tabla tipo
    tipo_id = db.Column(db.Integer, db.ForeignKey('tipo.id'), nullable=True)
    # para acceder al tipo
    tipo = db.relationship('Tipo', backref=db.backref('servicios', lazy=True))
    habilitado = db.Column(db.Boolean, nullable=False, default=True)

    # asignar a la institucion activa,sacar el mail de la session
    institucion_id = db.Column(db.Integer, db.ForeignKey('institucion.id'))

    institucion = db.relationship(
        'Institucion', backref=db.backref('servicios', lazy=True))

    def __init__(
        self, nombre=None, descripcion=None, palabras_claves=None,
        habilitado=None, tipo_id=None, institucion_id=None
    ):
        self.nombre = nombre
        self.descripcion = descripcion
        self.palabras_claves = palabras_claves
        self.habilitado = habilitado
        self.tipo_id = tipo_id
        self.institucion_id = institucion_id
