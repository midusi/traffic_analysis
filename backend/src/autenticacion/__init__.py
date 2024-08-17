from src.core.database import db
from src.core.autenticacion.usuario import Usuario
from src.core.institucion.models.institucion import Institucion
from src.core.institucion import get_institucion_by_id
from core.autenticacion.bcrypt import bcrypt
from src.core.autenticacion.roles_y_permisos import Usuario_Tiene_Rol, Rol
from src.core.usuarios_institucion import agregar_user_rol_institucion


def listar_usuarios():
    return Usuario.query.all()


def listar_usuarios_paginated(page, per_page, email=None, activo=None):
    """Retorna una lista con los usuarios paginados, no muestra aquellos usuarios con rol de super admin"""
    subquery = (
        db.session.query(Usuario.id)
        .join(Usuario.usuario_tiene_rol)
        .join(Rol)
        .filter(Rol.nombre == "superadmin")
    )
    usuarios = Usuario.query.filter(Usuario.id.notin_(subquery))
    # usuarios = Usuario.query
    if email:
        usuarios = usuarios.filter(Usuario.email.ilike(f"%{email}%"))
    if activo is not None and activo in ["0", "1"]:
        usuarios = usuarios.filter(Usuario.activo == bool(int(activo)))

    usuarios = usuarios.order_by(Usuario.email).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return usuarios


def crear_usuario_simple(nombre, apellido, email):
    """
    Crea un usuario para la primera fase del registro
    """
    usuario = Usuario(
        nombre=nombre,
        apellido=apellido,
        email=email,
        # activo=False,
    )
    db.session.add(usuario)
    db.session.commit()




def completar_usuario(email, username, password):
    """
    Completa al usuario creado en la primera fase
    """
    hash = bcrypt.generate_password_hash(password.encode("utf-8"))
    password = hash.decode("utf-8")

    usuario = buscar_usuario_por_email(email)

    usuario.username = username
    usuario.password = password
    usuario.activo = True

    db.session.commit()



def crear_usuario(**kwargs):
    """Crea un usuario"""
    crear_usuario_simple(kwargs["nombre"], kwargs["apellido"], kwargs["email"])
    completar_usuario(kwargs["email"], kwargs["username"], kwargs["password"])
    if kwargs["institucion"] == "no_tiene":
        agregar_user_rol_institucion(
            email=kwargs["email"], nombre_rol=kwargs["rol"], id_institucion=""
        )
    else:
        institucion = Institucion.query.filter_by(nombre=kwargs["institucion"]).first()
        agregar_user_rol_institucion(
            email=kwargs["email"],
            nombre_rol=kwargs["rol"],
            id_institucion=institucion.id,
        )
        usuario = Usuario.query.filter_by(email=kwargs["email"]).first()
        asignar_institucion_activa(usuario.id, institucion.id)

    # usuario = Usuario(**kwargs)
    # db.session.add(usuario)
    # db.session.commit()

    # return usuario


"""def agregar_user_rol_institucion(email, nombre_rol, nombre_institucion):
    user = Usuario.query.filter_by(email=email).first()
    rol = Rol.query.filter_by(nombre=nombre_rol).first()
    institucion = Institucion.query.filter_by(nombre=nombre_institucion).first()
    print(rol, institucion, user)
    rol_inst = Usuario_Tiene_Rol(rol.id, institucion.id, user.id)
    db.session.add(rol_inst)
    db.session.commit()"""


def agregar_rol_a_usuario(rol, user, institucion):
    """Agrega un rol a un usuario en la institucion dada. En caso de ser superadmin no agrega la institucion."""
    rol = Rol.query.filter_by(nombre=rol).first()
    user = buscar_usuario_por_email(user)
    institucion = Institucion.query.filter_by(nombre=institucion).first()
    if rol.nombre == "superadmin":
        rol_inst = Usuario_Tiene_Rol(
            rol_id=rol.id, usuario_id=user.id, institucion_id=None
        )
    else:
        rol_inst = Usuario_Tiene_Rol(rol.id, institucion.id, user.id)
    db.session.add(rol_inst)
    db.session.commit()


def agregar_permiso_a_rol(permiso, rol):
    """Agrega un rol a un permiso"""
    rol.permisos.append(permiso)
    db.session.commit()


def buscar_usuario_por_email(email):
    """Devuelve al usuario con el email dado"""
    return Usuario.query.filter_by(email=email).first()


def buscar_usuario_por_username(username):
    """Devuelve al usuario con el username dado"""
    return Usuario.query.filter_by(username=username).first()


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


"""
def listar_permisos_por_email_usuario(email):
    usuario = buscar_usuario_por_email(email)
    usuario_tiene_rol = Usuario_Tiene_Rol.query.filter_by(usuario_id=usuario.id)
    permisos_usuario = []

    for user_rol in usuario_tiene_rol:
        permisos = Rol.query.filter_by(id=user_rol.rol_id).first().permisos
        for permiso in permisos:
            permisos_usuario.append(permiso.nombre)

    return permisos_usuario
"""


def listar_permisos_por_email_usuario(email):
    """Consigue todos los permisos de un usuario con el email dado"""
    usuario = buscar_usuario_por_email(email)
    usuario_tiene_rol = Usuario_Tiene_Rol.query.filter_by(usuario_id=usuario.id)
    permisos_usuario = []

    for user_rol in usuario_tiene_rol:
        rol = Rol.query.filter_by(id=user_rol.rol_id).first()
        print(rol)
        if rol:
            permisos = rol.permisos
            print(permisos)
            for permiso in permisos:
                permisos_usuario.append(permiso.nombre)
    return permisos_usuario


def listar_permisos_por_email_usuario_institucion(email):
    """Lista todos los permisos de la institucion activa de un usuario dado su email"""
    usuario = buscar_usuario_por_email(email)
    usuario_tiene_rol = Usuario_Tiene_Rol.query.filter_by(
        usuario_id=usuario.id, institucion_id=usuario.institucion_activa_id
    )
    permisos_usuario = []

    for user_rol in usuario_tiene_rol:
        rol = Rol.query.filter_by(id=user_rol.rol_id).first()
        print(rol)
        if rol:
            permisos = rol.permisos
            print(permisos)
            for permiso in permisos:
                permisos_usuario.append(permiso.nombre)
    return permisos_usuario



def update_usuario(**kwargs):
    """Actualiza los datos de un usuario"""
    usuario = buscar_usuario_por_id(kwargs["id"])
    usuario.username = kwargs["username"]
    usuario.email = kwargs["email"]
    usuario.nombre = kwargs["nombre"]
    usuario.apellido = kwargs["apellido"]
    # usuario.activo = kwargs["activo"]
    # usuario.created_at = kwargs["created_at"]
    # usuario.updated_at = kwargs["updated_at"]

    db.session.commit()



def delete_usuario(id):
    """Elimina un usuario"""
    registros_relacionados = Usuario_Tiene_Rol.query.filter_by(usuario_id=id).all()
    for registro in registros_relacionados:
        db.session.delete(registro)

    Usuario.query.filter_by(id=id).delete()
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


def get_usuario_institucion_activa(id):
    """Retorna la institucion activa de un usuario dado su id"""
    usuario = Usuario.query.filter_by(id=id).first()

    if usuario:
        institucion_activa = Institucion.query.get(usuario.institucion_activa_id)
        return institucion_activa
    else:
        return None  


def get_instituciones_by_id(user_id):
    """Retorna las instituciones de un usuario dado su id"""
    usuario = Usuario.query.get(user_id)

    if usuario:
        instituciones = (
            db.session.query(
                Institucion
            )  
            .join(Usuario_Tiene_Rol)  # Realiza una unión con Usuario_Tiene_Rol
            .filter(Usuario_Tiene_Rol.usuario_id == usuario.id)
            .all()
        )
        return instituciones
    else:
        return []


def agregar_institucion_a_usuario(usuario_id, institucion_id,rol_id):
    usuario = Usuario.query.get(usuario_id)

    if usuario:
        institucion = Institucion.query.get(institucion_id)

        if institucion:
            if institucion not in usuario.usuario_tiene_rol:
                usuario_tiene_rol = Usuario_Tiene_Rol(
                    usuario_id=usuario_id, rol_id=None, institucion_id=institucion_id
                )
                db.session.add(usuario_tiene_rol)
                db.session.commit()
                print(usuario_tiene_rol.institucion.nombre)
                print(usuario_tiene_rol.usuario.nombre)
                return True
            else:
                print("La institución ya está relacionada con el usuario.")
                return "La institución ya está relacionada con el usuario."

        else:
            print("La institución con el ID especificado no existe.")
            return "La institución con el ID especificado no existe."

    else:
        print("El usuario con el ID especificado no existe.")
        return "El usuario con el ID especificado no existe."


def asignar_institucion_activa(usuario_id, institucion_id):
    """Asigna una institucion activa a un usuario"""
    usuario = Usuario.query.get(usuario_id)
    institucion = Institucion.query.get(institucion_id)

    if usuario and institucion:
        usuario.institucion_activa = institucion

        db.session.commit()

        return True
    else:
        return "El usuario o la institución con el ID especificado no existen."


def obtener_todos_los_roles():
    """Retorna todos los roles del sistema"""
    return Rol.query.all()


def list_roles():
    return Rol.query.all()


def esta_activo(email):
    """Verifica si el usuario con el email dado esta activo"""
    usuario = buscar_usuario_por_email(email)
    return usuario.activo


def es_superadmin(email):
    user = buscar_usuario_por_email(email)
    return (
        Usuario_Tiene_Rol.query.filter_by(usuario_id=user.id)
        .filter_by(rol_id=1)
        .first()
    )

def es_dueño(email):
    user = buscar_usuario_por_email(email)
    return (
        Usuario_Tiene_Rol.query.filter_by(usuario_id=user.id)
        .filter_by(rol_id=2)
        .first()
    )
