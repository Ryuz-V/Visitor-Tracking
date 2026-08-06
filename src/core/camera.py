import cv2

class VideoStream:
    def __init__(self, source=0):
        # Inisialisasi penangkapan video (0 untuk webcam default)
        self.cap = cv2.VideoCapture(source)
        
    def get_resolution(self):
        # Mengambil lebar dan tinggi resolusi kamera
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return width, height
        
    def is_opened(self):
        # Mengecek apakah kamera berhasil terhubung
        return self.cap.isOpened()
        
    def read(self):
        # Membaca video frame per frame
        return self.cap.read()
        
    def release(self):
        # Melepaskan penggunaan kamera dari memori setelah selesai
        self.cap.release()