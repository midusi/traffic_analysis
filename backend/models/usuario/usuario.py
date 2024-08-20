from enum import unique
from backend.models.database import db
import secrets
from datetime import datetime, timedelta


class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    password = db.Column(db.String(255))
    email = db.Column(db.String(50), nullable=False, unique=True)
    nombre = db.Column(db.String(25), nullable=True)
    apellido = db.Column(db.String(25), nullable=True)
    admin = db.Column(db.Boolean, nullable=False)
    activo = db.Column(db.Boolean, nullable=False)
    token = db.Column(db.String(255), nullable=True, unique=True)
    token_expiracion = db.Column(db.DateTime, nullable=True)
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
        self.token = secrets.token_urlsafe(16)
        self.token_expiracion = datetime.now() + timedelta(
            days=30
        )  # Token válido por 1 mes, si usa recuperar contraseña se deberia setear en 1 día

    def __repr__(self):
        return f"<Usuario {self.email}>"
