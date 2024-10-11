cola_videos = []

def encolar(data):
    """
    data deberia tener el path del video, la resolución y los poligonos con sus datos
    """
    if(len(cola_videos) == 0):
        procesar(data)
    else:
        cola_videos.append(data)

def procesar(data):
    """
    generar n-1 threads (dejando 1 para el server?)
    enviar frames/n a cada hilo
    (tmbn esto se podria hacer en otro server)
    """
    # modelo(data)
    cola_videos.pop(data)
    # videos.CambiarEstado(data['video_path'], 'procesado')
