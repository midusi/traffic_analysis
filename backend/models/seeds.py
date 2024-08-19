from backend.models import prueba
from backend.models.database import db
from backend.models.usuario import crear_usuario_password


def run():

    print("Cargando datos...")

    prueba_1 = prueba.create_prueba(name="Prueba 1")
    prueba_2 = prueba.create_prueba(name="Prueba 2")

    crear_usuario_password(
        nombre="Admin",
        apellido="Messi",
        email="admin@gmail.com",
        admin=True,
        password="admin",
    )

    print("Datos cargados, izi")
