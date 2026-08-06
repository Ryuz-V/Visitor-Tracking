import cv2
from ultralytics import YOLO
import supervision as sv

class PeopleTracker:
    def __init__(self, frame_width, frame_height):
        # Memuat model YOLOv8 versi nano (paling ringan) untuk deteksi objek
        # YOLO akan otomatis men-download 'yolov8n.pt' pada percobaan pertama jika file belum ada
        self.model = YOLO("yolov8n.pt")
        
        # Membuat titik awal (kiri) dan akhir (kanan) untuk garis penghitung
        # Posisinya diletakkan tepat di tengah layar secara horizontal
        start = sv.Point(0, frame_height // 2)
        end = sv.Point(frame_width, frame_height // 2)
        self.line_zone = sv.LineZone(start=start, end=end)
        
        # Inisialisasi alat-alat dari supervision untuk menggambar hasil deteksi
        self.box_annotator = sv.BoxAnnotator()
        self.label_annotator = sv.LabelAnnotator()
        self.line_annotator = sv.LineZoneAnnotator(thickness=2, text_thickness=2, text_scale=1)
        
        # Menyimpan hitungan sebelumnya agar kita tahu jika ada penambahan
        self.prev_in_count = 0

    def process_frame(self, frame):
        # Melakukan tracking objek
        # classes=[0] memastikan model HANYA mendeteksi manusia (ID 0 pada class COCO)
        results = self.model.track(
            frame, 
            classes=[0], 
            persist=True, 
            tracker="bytetrack.yaml", 
            verbose=False
        )[0]
        
        # Mengonversi format hasil YOLO menjadi format supervision
        detections = sv.Detections.from_ultralytics(results)
        
        # Men-trigger logika garis penghitung dengan data deteksi saat ini
        self.line_zone.trigger(detections=detections)
        
        # Menghitung selisih jumlah masuk yang baru dideteksi pada frame ini
        current_in = self.line_zone.in_count
        new_in = current_in - self.prev_in_count
        self.prev_in_count = current_in
        
        # Menyiapkan label berupa ID Tracker untuk setiap objek yang terdeteksi
        labels = [
            f"#{tracker_id} Orang"
            for tracker_id in detections.tracker_id
        ] if detections.tracker_id is not None else []
        
        # Menggambar kotak pembatas (bounding box), label, dan garis pada frame video
        annotated_frame = self.box_annotator.annotate(scene=frame.copy(), detections=detections)
        annotated_frame = self.label_annotator.annotate(scene=annotated_frame, detections=detections, labels=labels)
        self.line_annotator.annotate(frame=annotated_frame, line_counter=self.line_zone)
        
        # Mengembalikan frame yang sudah digambar dan jumlah objek baru yang melewati garis
        return annotated_frame, new_in