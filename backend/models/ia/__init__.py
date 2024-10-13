import os
from .example import run

cola_videos = []

def encolar(data):
    """
    data tiene el path del video, la resolución y los poligonos con sus datos (tipo,nombre, lista de puntos)
    """
    #esta funcion solo tendria que encolar porque sino traba la request de front
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
    if(not data):
        cola_videos.pop(data)

    # videos.CambiarEstado(data['video_path'], 'procesando')

    nombre_video = data.get('path')
    path_abs = os.path.join(os.getcwd(), "models", "ia")
    source_video_path = os.path.join(path_abs, nombre_video)
    source_weights_path = os.path.join(path_abs, "traffic_analysis.pt")
    target_video_path = os.path.join(path_abs, "resultados", nombre_video)
    confidence_threshold = 0.3
    iou_threshold = 0.7

    print("Antes de procesar")
    run(
        source_weights_path=source_weights_path,
        source_video_path=source_video_path,
        target_video_path=target_video_path,
        confidence_threshold=confidence_threshold,
        iou_threshold=iou_threshold
    )
    print("Después de procesar")

    # videos.CambiarEstado(data['video_path'], 'finalizado')
    # volver a ejecutar procesar si la lista no esta vacia?
