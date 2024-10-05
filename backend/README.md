Para ejecutar el backend hay que:
*Tener poetry y python instalados
*Tener MySQL instalado y corriendo
*Chequear tener lo necesario para mysqlclient (ver https://pypi.org/project/mysqlclient/ en la seccion de install en linux)

*Instalar las dependencias del proyecto
```
poetry install
```

*Inicializar la BD
```
poetry run flask resetdb
poetry run flask seedsdb
```

*Levantar el servidor
```
poetry run flask run
```



