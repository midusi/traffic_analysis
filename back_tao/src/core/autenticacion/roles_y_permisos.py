from src.core.database import db


rol_tiene_permiso = db.Table(
    "rol_tiene_permiso",
    db.Column("rol_id", db.Integer, db.ForeignKey("rol.id")),
    db.Column("permiso_id", db.Integer, db.ForeignKey("permiso.id")),
)

#TODO en el crud, debo poder asignarle un rol a un usuario
class Rol(db.Model):
    __tablename__ = "rol"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String(25), nullable=False)

    permisos = db.relationship("Permiso", secondary=rol_tiene_permiso, backref="rol")

    def __init__(self, nombre=None):
        self.nombre = nombre

    def __repr__(self):
        return f"<Rol {self.nombre}>"


class Permiso(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    nombre = db.Column(db.String(25), nullable=False)

    def __init__(self, nombre=None):
        self.nombre = nombre

    def __repr__(self):
        return f"<Permiso {self.nombre}>"


class Usuario_Tiene_Rol(db.Model):
    __tablename__ = "usuario_tiene_rol"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    rol_id = db.Column(db.Integer, db.ForeignKey("rol.id"))
    institucion_id = db.Column(db.Integer, db.ForeignKey("institucion.id"))


    usuario = db.relationship("Usuario", backref="usuario_tiene_rol")
    rol = db.relationship("Rol", backref="usuario_tiene_rol")
    institucion = db.relationship("Institucion", backref="usuario_tiene_rol")

    def __init__(self, rol_id=None, institucion_id=None, usuario_id=None):
        self.usuario_id = usuario_id
        self.rol_id = rol_id
        self.institucion_id = institucion_id
