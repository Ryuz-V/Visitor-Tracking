import cv2
from ultralytics import YOLO
import supervision as sv

class PeopleTracker:
    def __init__(self, frame_width, frame_height):
        # Memuat model YOLOv8 versi nano
        self.model = YOLO("yolov8n.pt")
        
        # Garis virtual penghitung pengunjung (DIUBAH MENJADI VERTIKAL)
        # Membentang dari atas (0) ke bawah (frame_height) pada posisi tengah lebar layar
        start = sv.Point(frame_width // 2, 0)
        end = sv.Point(frame_width // 2, frame_height)
        self.line_zone = sv.LineZone(start=start, end=end)
        
        # Inisialisasi alat gambar
        self.box_annotator = sv.BoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()
        self.line_annotator = sv.LineZoneAnnotator(thickness=2, text_thickness=2, text_scale=1)
        
        self.prev_in_count = 0

    def process_frame(self, frame):
        # 1. TRACKING SEMUA OBJEK
        results = self.model.track(
            frame, 
            persist=True, 
            tracker="bytetrack.yaml", 
            verbose=False
        )[0]
        
        # Konversi ke format Supervision
        detections = sv.Detections.from_ultralytics(results)
        
        # 2. FILTERING UNTUK GARIS (Hanya menghitung manusia)
        # class_id 0 pada YOLO adalah 'person'
        human_detections = detections[detections.class_id == 0]
        
        # Trigger garis hanya menggunakan data manusia
        self.line_zone.trigger(detections=human_detections)
        
        # Hitung selisih pengunjung masuk
        current_in = self.line_zone.in_count
        new_in = current_in - self.prev_in_count
        self.prev_in_count = current_in
        
        # 3. LOGIKA PELABELAN KOTAK (Visitor vs Anomali)
        labels = []
        for i in range(len(detections)):
            class_id = detections.class_id[i]
            
            # Ambil ID pelacakan jika sudah tersedia
            tracker_id = None
            if detections.tracker_id is not None:
                tracker_id = detections.tracker_id[i]
                
            # Ambil nama asli objek dari kecerdasan YOLO
            class_name = self.model.names[class_id]
            
            if class_id == 0:
                # Jika objek adalah MANUSIA
                if tracker_id is not None:
                    labels.append(f"#{tracker_id} Visitor")
                else:
                    labels.append("Visitor")
            else:
                labels.append(f"ANOMALY: {class_name.upper()}")
                
        annotated_frame = self.box_annotator.annotate(scene=frame.copy(), detections=detections)
        annotated_frame = self.label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)
        self.line_annotator.annotate(frame=annotated_frame, line_counter=self.line_zone)
        
        return annotated_frame, new_in