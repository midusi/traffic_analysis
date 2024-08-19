from backend.models.database import db


class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(50), nullable=False, unique=True)
    nombre = db.Column(db.String(25), nullable=True)
    apellido = db.Column(db.String(25), nullable=True)
    admin = db.Column(db.Boolean, nullable=False)
    activo = db.Column(db.Boolean, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    def __init__(
        self,
        password=None,
        email=None,
        nombre=None,
        apellido=None,
        admin=None,
    ):
        self.email = email
        self.password = password
        self.nombre = nombre
        self.apellido = apellido
        self.admin = admin
        self.activo = True

    def __repr__(self):
        return f"<Usuario {self.email}>"
