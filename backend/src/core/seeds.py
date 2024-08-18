from src.core.models import prueba

def run():

     print("Cargando datos...")

     prueba_1 = prueba.create_prueba(name="Prueba 1")
     prueba_2 = prueba.create_prueba(name="Prueba 2")

     print("Datos cargados, izi")