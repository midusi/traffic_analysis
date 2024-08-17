from src.core.database import db
from datetime import datetime
from src.core.autenticacion.roles_y_permisos import Usuario_Tiene_Rol


#Tabla intermedia para la relacion entre un usuario y sus instituciones
usuarios_instituciones = db.Table(
    'usuarios_instituciones',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id')),
    db.Column('institucion_id', db.Integer, db.ForeignKey('institucion.id'))
)

class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(50), nullable=False, unique=True)
    nombre = db.Column(db.String(25), nullable=False)
    apellido = db.Column(db.String(25), nullable=False)
    activo = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Define el campo 'institucion_activa' que apunta a una institución
    institucion_activa_id = db.Column(db.Integer, db.ForeignKey('institucion.id'))
    institucion_activa = db.relationship('Institucion', foreign_keys=[institucion_activa_id])

    # rol_institucion = db.Column(db.Integer(), db.ForeignKey("usuario_tiene_rol.id"))


    def __init__(
        self,
        username=None,
        password=None,
        email=None,
        nombre=None,
        apellido=None,
        #activo=None,
    ):
        self.username = username
        self.password = password
        self.email = email
        self.nombre = nombre
        self.apellido = apellido
        self.institucion=None
        self.institucion_id=None
        self.activo=True

    def __repr__(self):
        return f"<Usuario {self.username}>"
