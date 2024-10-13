from typing import Dict, Iterable, List, Set
import cv2
import numpy as np
from tqdm import tqdm
from ultralytics import YOLO
import supervision as sv

COLORS = sv.ColorPalette.from_hex(["#E6194B", "#3CB44B", "#FFE119", "#3C76D1"])

#### Polygons para usar en el video otro_minuto
ZONE_IN_POLYGONS = [
    # np.array([[980, 282], [1120, 262], [1210, 82], [1140, 82]]), #ROJO
    # np.array([[850, 850], [1050, 900], [950, 1060], [730, 1060]]), #VERDE
    # np.array([[300, 400], [300, 460], [65, 410], [65, 360]]), #AMARILLO
    # np.array([[1450, 492], [1450, 600], [1750, 690], [1920, 510]]), #AZUL
]

ZONE_OUT_POLYGONS = [
    np.array([[1120, 282], [1240, 282], [1280, 82], [1220, 82]]), #ROJO
    np.array([[615, 860], [730, 860], [725, 1060], [580, 1060]]), #VERDE
    np.array([[300, 320], [300, 380], [65, 330], [65, 282]]), #AMARILLO
    np.array([[1440, 690], [1450, 780], [1750, 790], [1750, 700]]), #AZUL
]

class DetectionsManager:
    def __init__(self) -> None:
        self.tracker_id_to_zone_id: Dict[int, int] = {}
        self.counts: Dict[int, Dict[int, Set[int]]] = {}

    def update(
        self,
        detections_all: sv.Detections,
        detections_in_zones: List[sv.Detections],
        detections_out_zones: List[sv.Detections],
    ) -> sv.Detections:
        for zone_in_id, detections_in_zone in enumerate(detections_in_zones):
            for tracker_id in detections_in_zone.tracker_id:
                self.tracker_id_to_zone_id.setdefault(tracker_id, zone_in_id)

        for zone_out_id, detections_out_zone in enumerate(detections_out_zones):
            for tracker_id in detections_out_zone.tracker_id:
                if tracker_id in self.tracker_id_to_zone_id:
                    zone_in_id = self.tracker_id_to_zone_id[tracker_id]
                    self.counts.setdefault(zone_out_id, {})
                    self.counts[zone_out_id].setdefault(zone_in_id, set())
                    self.counts[zone_out_id][zone_in_id].add(tracker_id)
        if len(detections_all) > 0:
            detections_all.class_id = np.vectorize(
                lambda x: self.tracker_id_to_zone_id.get(x, -1)
            )(detections_all.tracker_id)
        else:
            detections_all.class_id = np.array([], dtype=int)
        return detections_all[detections_all.class_id != -1]


def initiate_polygon_zones(
    polygons: List[np.ndarray],
    triggering_anchors: Iterable[sv.Position] = [sv.Position.CENTER],
) -> List[sv.PolygonZone]:
    return [
        sv.PolygonZone(
            polygon=polygon,
            triggering_anchors=triggering_anchors,
        )
        for polygon in polygons
    ]


class VideoProcessor:
    def __init__(
        self,
        source_weights_path: str,
        source_video_path: str,
        target_video_path: str,
        confidence_threshold: float = 0.3,
        iou_threshold: float = 0.7,
    ) -> None:
        self.conf_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        self.source_video_path = source_video_path
        self.target_video_path = target_video_path

        self.model = YOLO(source_weights_path)
        self.tracker = sv.ByteTrack()

        self.video_info = sv.VideoInfo.from_video_path(source_video_path)
        self.zones_in = []
        self.zones_out = []

        self.box_annotator = sv.BoxAnnotator(color=COLORS)
        self.label_annotator = sv.LabelAnnotator(
            color=COLORS, text_color=sv.Color.BLACK
        )
        self.trace_annotator = sv.TraceAnnotator(
            color=COLORS, position=sv.Position.CENTER, trace_length=100, thickness=2
        )
        self.detections_manager = DetectionsManager()
        self.classes = {
            "car": "Auto",
            "bus": "Colectivo",
            "truck": "Camión",
            "van": "Camioneta",
        }

    def get_confidence(self, confidence: float):
        return "{:.0f}%".format(confidence * 100)

    def process_video(self):
        frame_generator = sv.get_video_frames_generator(
            source_path=self.source_video_path
        )

        scalar_x = self.video_info.width / 800
        scalar_y = self.video_info.height / 450
        original_polygon = np.array(
            [
                [312.4444274902344,425.0173568725586],
                [373.4444274902344,363.0173568725586],
                [423.4444274902344,347.0173568725586],
                [451.4444274902344,370.0173568725586],
                [351.4444274902344,443.0173568725586]
            ])

        # Redimensionar el polígono e inicializar zonas
        resized_polygon = np.array([[x * scalar_x, y * scalar_y] for x, y in original_polygon]).astype(np.int32)
        self.zones_in = initiate_polygon_zones([resized_polygon], [sv.Position.CENTER])
        self.zones_out = initiate_polygon_zones(ZONE_OUT_POLYGONS, [sv.Position.CENTER])

        if self.target_video_path:
            with sv.VideoSink(self.target_video_path, self.video_info) as sink:
                for frame in tqdm(frame_generator, total=self.video_info.total_frames):
                    annotated_frame = self.process_frame(frame)
                    sink.write_frame(annotated_frame)
        else:
            for frame in tqdm(frame_generator, total=self.video_info.total_frames):
                annotated_frame = self.process_frame(frame)
                cv2.imshow("Processed Video", annotated_frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            cv2.destroyAllWindows()

    def annotate_frame(
        self, frame: np.ndarray, detections: sv.Detections
    ) -> np.ndarray:
        annotated_frame = frame.copy()
        for i, (zone_in, zone_out) in enumerate(zip(self.zones_in, self.zones_out)):
            annotated_frame = sv.draw_polygon(
                annotated_frame, zone_in.polygon, COLORS.colors[i]
            )
            annotated_frame = sv.draw_polygon(
                annotated_frame, zone_out.polygon, COLORS.colors[i]
            )

        # labels a visualizar en el Bounding Box
        labels = [f"{self.classes[class_name]} - {self.get_confidence(confidence)}" for class_name, confidence in zip(detections.data["class_name"], detections.confidence)]
        annotated_frame = self.trace_annotator.annotate(annotated_frame, detections)
        annotated_frame = self.box_annotator.annotate(annotated_frame, detections)
        annotated_frame = self.label_annotator.annotate(
            annotated_frame, detections, labels
        )

        for zone_out_id, zone_out in enumerate(self.zones_out):
            zone_center = sv.get_polygon_center(polygon=zone_out.polygon)
            if zone_out_id in self.detections_manager.counts:
                counts = self.detections_manager.counts[zone_out_id]
                for i, zone_in_id in enumerate(counts):
                    count = len(self.detections_manager.counts[zone_out_id][zone_in_id])
                    text_anchor = sv.Point(x=zone_center.x, y=zone_center.y + 40 * i)
                    annotated_frame = sv.draw_text(
                        scene=annotated_frame,
                        text=str(count),
                        text_anchor=text_anchor,
                        background_color=COLORS.colors[zone_in_id],
                    )

        return annotated_frame

    def process_frame(self, frame: np.ndarray) -> np.ndarray:
        results = self.model(
            frame, verbose=False, imgsz=1280, conf=self.conf_threshold, iou=self.iou_threshold
        )[0]
        detections = sv.Detections.from_ultralytics(results) # Obtiene los resultados de las detecciones
        detections.class_id = np.zeros(len(detections)) # Crea un arreglo con tantas posiciones como objetos detectados
        detections = self.tracker.update_with_detections(detections)

        detections_in_zones = []
        detections_out_zones = []

        for zone_in, zone_out in zip(self.zones_in, self.zones_out):
            detections_in_zone = detections[zone_in.trigger(detections=detections)]
            detections_in_zones.append(detections_in_zone)
            detections_out_zone = detections[zone_out.trigger(detections=detections)]
            detections_out_zones.append(detections_out_zone)

        detections = self.detections_manager.update(
            detections, detections_in_zones, detections_out_zones
        )
        return self.annotate_frame(frame, detections)

def run(
    source_weights_path: str,
    source_video_path: str,
    target_video_path: str = None,
    confidence_threshold: float = 0.3,
    iou_threshold: float = 0.7
):
    processor = VideoProcessor(
        source_weights_path=source_weights_path,
        source_video_path=source_video_path,
        target_video_path=target_video_path,
        confidence_threshold=confidence_threshold,
        iou_threshold=iou_threshold,
    )
    processor.process_video()
