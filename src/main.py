import cv2
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.config.settings import CAMERA_SOURCE
from src.core.camera import VideoStream
from src.core.tracker import PeopleTracker
from src.database.queries import catat_pengunjung

def main():
    print("Memulai sistem Human Tracking...")
    video_stream = VideoStream(source=CAMERA_SOURCE)
    
    # ... (Sisa kode main.py sama persis seperti sebelumnya) ...
    
    # 1. Inisialisasi Kamera (0 untuk webcam laptop, atau bisa diganti RTSP URL)
    video_stream = VideoStream(source=0)
    
    # 2. Inisialisasi Tracker AI (YOLOv8 + Supervision LineZone)
    frame_width, frame_height = video_stream.get_resolution()
    tracker = PeopleTracker(frame_width, frame_height)
    
    print("Sistem berjalan. Tekan 'q' pada keyboard untuk keluar.")

    while video_stream.is_opened():
        ret, frame = video_stream.read()
        if not ret:
            print("Gagal membaca frame dari kamera.")
            break
            
        # 3. Proses frame melalui AI & deteksi garis lintas
        # Melacak objek dengan class=0 (Manusia)
        annotated_frame, crossed_in = tracker.process_frame(frame)
        
        # 4. Jika ada orang yang melewati garis masuk (IN)
        if crossed_in > 0:
            print(f"[INFO] Pengunjung masuk terdeteksi! Menambahkan ke database...")
            # Panggil fungsi database untuk update data harian
            catat_pengunjung(jumlah=crossed_in)

        # 5. Tampilkan hasil visual ke layar
        cv2.imshow("Advanced People Counting System", annotated_frame)

        # Tombol 'q' untuk berhenti
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_stream.release()
    cv2.destroyAllWindows()
    print("Sistem dihentikan dengan aman.")

if __name__ == "__main__":
    main()