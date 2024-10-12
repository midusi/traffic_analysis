import sys
from .example import run

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
    if(len(cola_videos) != 0):
        cola_videos.pop(data)

    # videos.CambiarEstado(data['video_path'], 'procesado')
     
    # Simula la llamada como si fuera desde la terminal
    sys.argv = [
        "example.py",
        "--source_weights_path", "/home/tao/civil/proyecto_civil/backend/models/ia/traffic_analysis.pt",
        "--source_video_path", "/home/tao/civil/proyecto_civil/backend/models/ia/otro minuto.mp4",
        "--iou_threshold", "0.5",
        "--target_video_path", "/home/tao/civil/proyecto_civil/backend/models/ia/traffic_analysis_result.mp4"
    ]

    print("Antes de procesar")
    # Llama a la función `run` para probarla
    run()   
    print("Despues de procesar")

