from flask import request


def es_produccion():
    """Determina si la aplicación se está ejecutando en el servidor de producción o no.
    :return: (bool) True si el código se está ejecutando en el servidor de producción, y False en caso contrario.
    """

    root_url = request.url_root
    developer_url = "http://localhost/"
    return root_url != developer_url


def conseguir_url():
    """Determina la URL de la aplicación.
    Dependiendo de si la aplicación se está ejecutando en el servidor de producción o no.
    """

    if es_produccion():
        return request.url_root
    else:
        return "http://127.0.0.1:5000/"
