from backend.models import prueba
from backend.models.database import db
from backend.models.usuario import crear_usuario


def run():

    print("Cargando datos...")

    prueba_1 = prueba.create_prueba(name="Prueba 1")
    prueba_2 = prueba.create_prueba(name="Prueba 2")
    prueba_3 = prueba.create_prueba(name="Prueba 3")
    prueba_4 = prueba.create_prueba(name="Prueba 4")
    prueba_5 = prueba.create_prueba(name="Prueba 5")
    prueba_6 = prueba.create_prueba(name="Prueba 6")
    prueba_7 = prueba.create_prueba(name="Prueba 7")
    prueba_8 = prueba.create_prueba(name="Prueba 8")

    crear_usuario(
        nombre="Admin",
        apellido="Messi",
        email="admin@gmail.com",
        admin=True,
        password="admin",
    )

    crear_usuario(
        nombre="No-admin",
        apellido="Comun",
        email="noadmin@gmail.com",
        admin=False,
        password="noadmin",
    )

    print("Datos cargados, izi")
