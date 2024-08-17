from src.core.database import db
from src.core.configuracion import create_configuracion, create_info_contacto
from src.core.database import db
from src.core.institucion.models.institucion import Institucion
from src.core.institucion import create_institucion, delete_institucion
from src.core.solicitudes import create_estado
from src.core.servicio import create_servicio, delete_servicio, create_tipo

from src.core.autenticacion.roles_y_permisos import Rol, Permiso
from src.core.autenticacion import (
    agregar_institucion_a_usuario,
    completar_usuario,
    crear_usuario_simple,
    agregar_rol_a_usuario,
    agregar_permiso_a_rol,
    crear_usuario,
)
from src.core.database import db

from src.core.institucion import create_institucion

from src.core.configuracion import create_configuracion, create_info_contacto


def run():
    """Crea datos iniciales en la base de datos"""
    print("Arrancando las seeds ")

    tipo1 = create_tipo(nombre="Tipo numero 1 !!!")

    tipo2 = create_tipo(nombre="Tipo numero 2 !!!")

    tipo3 = create_tipo(nombre="Tipo numero 3 !!!")

    print("seeds creadas")

    config = create_configuracion(
        cant_elementos_pag=10,
        mantenimiento=False,
        mantenimiento_msg="Estamos en mantenimiento",
    )



    info1 = create_info_contacto(nombre="Teléfono", activo=False)

    info2 = create_info_contacto(nombre="Email", activo=True)

    info3 = create_info_contacto(nombre="Dirección", activo=True)

    info4 = create_info_contacto(nombre="Sitio Web", activo=False)

    inst1 = (
        create_institucion(
            nombre="Institución 1",
            info="Informacion inst 1",
            direccion="direccion inst 1",
            localizacion="localizacion inst 2",
            web="institucion1.com",
            palabra_clave=["a", "b"],
            horario_atencion=["10-19"],
            email="no@mail.com",
            telefono=12345678,
        ),
    )
    inst2 = create_institucion(
        nombre="Institución 2",
        info="b",
        direccion="b",
        localizacion="d",
        web="d",
        palabra_clave=["d", "b"],
        horario_atencion=["11-12"],
        email="no@mail.com",
        telefono=12345678,
    )
    crear_usuario_simple(
        email="admin@gmail.com",
        nombre="admin",
        apellido="admin",
    )

    servicio1 = create_servicio(
        nombre="Servicio numero 1",
        descripcion="Esta es la descripcion del servicio 1",
        palabras_claves=["p. clave 1","p. clave 2"],
        habilitado=True,
        tipo_id=1, 
        institucion_id=1
    )

    servicio2 = create_servicio(
        nombre="Servicio numero 2",
        descripcion="Esta es la descripcion del servicio 2",
        palabras_claves=["p. clave 3","p. clave 4"],
        habilitado=True,
        tipo_id=2, 
        institucion_id=2
    )
    
    completar_usuario("admin@gmail.com", "admin", "admin")
    rol = Rol(nombre="superadmin")
    db.session.add(rol)
    db.session.commit()
    permiso1 = Permiso(nombre="institucion_index")
    permiso2 = Permiso(nombre="institucion_show")
    permiso3 = Permiso(nombre="institucion_update")
    permiso4 = Permiso(nombre="institucion_create")
    permiso5 = Permiso(nombre="institucion_destroy")
    permiso6 = Permiso(nombre="institucion_activate")
    permiso7 = Permiso(nombre="institucion_deactivate")
    permiso8 = Permiso(nombre="user_index")
    permiso9 = Permiso(nombre="user_show")
    permiso10 = Permiso(nombre="user_update")
    permiso11 = Permiso(nombre="user_create")
    permiso12 = Permiso(nombre="user_destroy")
    permiso13 = Permiso(nombre="user_activate")
    permiso14 = Permiso(nombre="user_deactivate")
    permiso15 = Permiso(nombre="user_instituciones")
    permiso16 = Permiso(nombre="user_activate_institucion")
    permiso17 = Permiso(nombre="user_filter")
    permiso_show = Permiso(nombre="configuracion_show")
    permiso_update = Permiso(nombre="configuracion_update")

    agregar_permiso_a_rol(permiso1, rol)
    agregar_permiso_a_rol(permiso2, rol)
    agregar_permiso_a_rol(permiso3, rol)
    agregar_permiso_a_rol(permiso4, rol)
    agregar_permiso_a_rol(permiso5, rol)
    agregar_permiso_a_rol(permiso6, rol)
    agregar_permiso_a_rol(permiso7, rol)
    agregar_permiso_a_rol(permiso7, rol)
    agregar_permiso_a_rol(permiso8, rol)
    agregar_permiso_a_rol(permiso9, rol)
    agregar_permiso_a_rol(permiso10, rol)
    agregar_permiso_a_rol(permiso11, rol)
    agregar_permiso_a_rol(permiso12, rol)
    agregar_permiso_a_rol(permiso13, rol)
    agregar_permiso_a_rol(permiso14, rol)
    agregar_permiso_a_rol(permiso15, rol)
    agregar_permiso_a_rol(permiso16, rol)
    agregar_permiso_a_rol(permiso17, rol)
    agregar_permiso_a_rol(permiso_show, rol)
    agregar_permiso_a_rol(permiso_update, rol)
    agregar_permiso_a_rol(permiso_show, rol)
    agregar_permiso_a_rol(permiso_update, rol)
    agregar_rol_a_usuario(rol="superadmin", institucion="", user="admin@gmail.com")

    crear_usuario_simple(
        email="duenio@gmail.com",
        nombre="dueño",
        apellido="dueño",
    )
    completar_usuario("duenio@gmail.com", "duenio", "duenio")
    permiso1 = Permiso(nombre="userinst_index")
    permiso2 = Permiso(nombre="userinst_create")
    permiso3 = Permiso(nombre="userinst_update")
    permiso4 = Permiso(nombre="userinst_destroy")

    # Para los servicios, el permiso de update te da permiso a habilitar/deshabilitar una institucion.
    permiso_servicio_1 = Permiso(nombre="servicio_update")
    permiso_servicio_2 = Permiso(nombre="servicio_create")
    permiso_servicio_3 = Permiso(nombre="servicio_destroy")
    permiso_servicio_4 = Permiso(nombre="servicio_index")
    permiso_servicio_5 = Permiso(nombre="servicio_show")
    permiso_solicitud_1 = Permiso(nombre="solicitudes_index")
    permiso_solicitud_2 = Permiso(nombre="solicitudes_show")
    permiso_solicitud_3 = Permiso(nombre="solicitudes_update")
    permiso_solicitud_4 = Permiso(nombre="solicitudes_destroy")

    rol = Rol(nombre="dueño")
    db.session.add(rol)
    db.session.commit()
    agregar_permiso_a_rol(permiso1, rol)
    agregar_permiso_a_rol(permiso2, rol)
    agregar_permiso_a_rol(permiso3, rol)
    agregar_permiso_a_rol(permiso4, rol)
    agregar_permiso_a_rol(permiso15, rol)
    agregar_permiso_a_rol(permiso16, rol)
    agregar_permiso_a_rol(permiso_servicio_1, rol)
    agregar_permiso_a_rol(permiso_servicio_2, rol)
    agregar_permiso_a_rol(permiso_servicio_3, rol)
    agregar_permiso_a_rol(permiso_servicio_4, rol)
    agregar_permiso_a_rol(permiso_servicio_5, rol)
    agregar_permiso_a_rol(permiso_solicitud_1, rol)
    agregar_permiso_a_rol(permiso_solicitud_2, rol)
    agregar_permiso_a_rol(permiso_solicitud_3, rol)
    agregar_permiso_a_rol(permiso_solicitud_4, rol)
    agregar_rol_a_usuario(
        rol="dueño", institucion="Institución 1", user="duenio@gmail.com"
    )

    # crear_usuario_simple(
    #     email="user@gmail.com",
    #     nombre="user",
    #     apellido="user",
    # )
    # completar_usuario("user@gmail.com", "user", "user")

    # crear_usuario_simple(
    #     email="user2@gmail.com",
    #     nombre="user2",
    #     apellido="user2",
    # )
    # completar_usuario("user2@gmail.com", "user2", "user2")

    rol = Rol(nombre="operador")
    db.session.add(rol)
    db.session.commit()
    agregar_permiso_a_rol(permiso_servicio_1, rol)
    agregar_permiso_a_rol(permiso_servicio_2, rol)
    agregar_permiso_a_rol(permiso_servicio_4, rol)
    agregar_permiso_a_rol(permiso_servicio_5, rol)
    rol = Rol(nombre="administrador")
    db.session.add(rol)
    db.session.commit()

    estado_pendiente = create_estado(nombre="Pendiente")
    estado_aceptada = create_estado(nombre="Aceptada")
    estado_rechazada = create_estado(nombre="Rechazada")
    estado_en_proceso = create_estado(nombre="En proceso")
    estado_finalizada = create_estado(nombre="Finalizada")
    estado_cancelada = create_estado(nombre="Cancelada")

    db.session.add(estado_pendiente)
    db.session.add(estado_aceptada)
    db.session.add(estado_rechazada)
    db.session.add(estado_en_proceso)
    db.session.add(estado_finalizada)
    db.session.add(estado_cancelada)
    db.session.commit()
