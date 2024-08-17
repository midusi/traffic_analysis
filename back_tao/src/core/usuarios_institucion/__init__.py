from src.core.database import db
from src.core.autenticacion.usuario import Usuario
from src.core.autenticacion.roles_y_permisos import Usuario_Tiene_Rol, Rol
from src.core.institucion.models.institucion import Institucion


def agregar_user_rol_institucion(email, nombre_rol, id_institucion):
    """
    Relaciona usuario con rol e institución.
    Recibe el email, el nombre del rol y el id de la institución.
    Primero busca el usuario por el mail.
    Después el rol por nombre.
    Luego verifica si la institución ya está relacionada al usuario.
    Si no está relacionada, crea y agrega el campo a Usuario_tiene_rol.
    """
    user = Usuario.query.filter_by(email=email).first()
    rol = Rol.query.filter_by(nombre=nombre_rol).first()
    
    if id_institucion != "":
        institucion = Institucion.query.filter_by(id=id_institucion).first()
        relacion_existente = Usuario_Tiene_Rol.query.filter_by(
            rol_id=rol.id, usuario_id=user.id, institucion_id=institucion.id
        ).first()
        
        if not relacion_existente:
            rol_inst = Usuario_Tiene_Rol(rol.id, institucion.id, user.id)
            db.session.add(rol_inst)
            db.session.commit()
        else:
            print("La institucion ya esta relacionada al usuario.")
    else:
        rol_inst = Usuario_Tiene_Rol(rol_id=rol.id, usuario_id=user.id)
        db.session.add(rol_inst)
        db.session.commit()



def get_usuarios_institucion(id_institucion):
    """
    Devuelve usuarios por institución y su rol.
    Recibe el id de la institución.
    Filtra por institución y por rol diferente a "Dueño".
    """

    usuarios = []
    user_rol = Usuario_Tiene_Rol.query.filter_by(institucion_id=id_institucion)
    for user in user_rol:
        usuario = Usuario.query.filter_by(id=user.usuario_id).first().email
        rol = Rol.query.filter_by(id=user.rol_id).first().nombre
        usuarios.append({"email": usuario, "rol": rol})
    return usuarios


def get_usuarios_institucion_paginated(id_institucion, page, per_page):
    """
    Lista todos los usuarios de una institución paginados.
    """
    rol_id_dueño = Rol.query.filter_by(nombre="dueño").first().id

    user_rol = (
        Usuario_Tiene_Rol.query.filter_by(institucion_id=id_institucion)
        .filter(Usuario_Tiene_Rol.rol_id != rol_id_dueño)
        .paginate(page=page, per_page=per_page, error_out=False)
    )
    return user_rol


def delete_rol(email, id_institucion):
    """
    Recibe un mail y un id de institución.
    Elimina el usuario que contenga esos datos.
    """

    user = Usuario.query.filter_by(email=email).first()
    Usuario_Tiene_Rol.query.filter_by(institucion_id=id_institucion).filter_by(
        usuario_id=user.id
    ).delete()
    db.session.commit()


def update_user_rol_institucion(email, rol, id_institucion):
    """
    Actualiza una tupla de la tabla.
    Recibe el email, el nombre del rol y el id de la institución.
    Primero busca el usuario por el mail.
    Luego la tupla de la tabla por user id e institución id.
    Después el rol por nombre.
    Finalmente actualiza el rol y agrega el campo a Usuario_tiene_rol.
    """
    user = Usuario.query.filter_by(email=email).first()
    user_rol = (
        Usuario_Tiene_Rol.query.filter_by(institucion_id=id_institucion)
        .filter_by(usuario_id=user.id)
        .first()
    )
    rol_search = Rol.query.filter_by(nombre=rol).first()
    user_rol.rol_id = rol_search.id
    db.session.commit()


def get_usuario(email, rol, id_institucion):
    """
    Devuelve un usuario a partir de un email y id_institución.
    """
    user = Usuario.query.filter_by(email=email).first()
    return (
        Usuario_Tiene_Rol.query.filter_by(institucion_id=id_institucion)
        .filter_by(usuario_id=user.id)
        .first()
    )
