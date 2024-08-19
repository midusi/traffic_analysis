from backend.models.database import db
from backend.models.usuario.usuario import Usuario
from backend.models.bcrypt import bcrypt
import secrets


def listar_usuarios():
    return Usuario.query.all()


def listar_usuarios_paginated(page, per_page, email=None, activo=None):
    """Retorna una lista con los usuarios paginados"""
    usuarios = listar_usuarios()

    if email:
        usuarios = usuarios.filter(Usuario.email.ilike(f"%{email}%"))

    usuarios = usuarios.order_by(Usuario.email).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return usuarios


def crear_usuario(nombre, apellido, email, admin):
    """
    Carga al usuario en la bd y le asigna una contraseña
    """

    org_password = secrets.token_urlsafe(10)
    password = hashear_password(org_password)

    usuario = Usuario(
        password=password, email=email, nombre=nombre, apellido=apellido, admin=admin
    )

    db.session.add(usuario)
    db.session.commit()

    # QUITAR ESTO
    return org_password


def crear_usuario_password(nombre, apellido, email, admin, password):
    """
    Carga al usuario en la bd y le asigna una contraseña
    """

    password = hashear_password(password)

    usuario = Usuario(
        password=password, email=email, nombre=nombre, apellido=apellido, admin=admin
    )

    db.session.add(usuario)
    db.session.commit()

    return usuario


def hashear_password(password):
    hash = bcrypt.generate_password_hash(password.encode("utf-8"))
    password = hash.decode("utf-8")
    return password


def buscar_usuario_por_email(email):
    """Devuelve al usuario con el email dado"""
    return Usuario.query.filter_by(email=email).first()


def buscar_usuario_por_id(id):
    """Devuelve al usuario con el id dado"""
    return Usuario.query.filter_by(id=id).first()


def chequear_usuario(email, password):
    """Devuelve al usuario con el email y password dados,
    si los datos son incorrectos devuelve None"""
    usuario = buscar_usuario_por_email(email)

    if usuario and bcrypt.check_password_hash(
        usuario.password, password.encode("utf-8")
    ):
        return usuario
    else:
        return None


def update_usuario(**kwargs):
    """Actualiza los datos de un usuario"""
    usuario = buscar_usuario_por_id(kwargs["id"])
    usuario.email = kwargs["email"]
    usuario.nombre = kwargs["nombre"]
    usuario.apellido = kwargs["apellido"]
    usuario.activo = kwargs["activo"]
    usuario.admin = kwargs["admin"]

    db.session.commit()


def activate_usuario(id):
    """Habilita a un usuario dado su id."""
    usuario = buscar_usuario_por_id(id)
    usuario.activo = True
    db.session.commit()


def deactivate_usuario(id):
    """Deshabilita a un usuario dado su id."""
    usuario = buscar_usuario_por_id(id)
    usuario.activo = False
    db.session.commit()


def esta_activo(email):
    """Verifica si el usuario con el email dado esta activo"""
    usuario = buscar_usuario_por_email(email)
    return usuario.activo


def es_admin(email):
    """Verifica si el usuario con el email dado es admin"""
    usuario = buscar_usuario_por_email(email)
    return usuario.admin
