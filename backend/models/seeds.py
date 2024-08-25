from backend.models import prueba

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

     print("Datos cargados, izi")