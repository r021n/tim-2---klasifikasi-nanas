from flask import Flask, request, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import os
import base64
from datetime import datetime
import cv2
from ultralytics import YOLO
import supervision as sv

app = Flask(__name__)
socketio = SocketIO(app)

class ImageProcessor(object):
    def __init__(self, image_path):
        self.image_path = image_path  # Menyimpan path gambar
        self.image = cv2.imread(image_path)  # Membaca gambar dari path folder
        self.model = YOLO("model\Best_600_epoch.pt")  # Memuat model YOLO yang telah dilatih
        self.box_annotator = sv.BoxAnnotator(  # Membuat objek BoxAnnotator untuk menggambar kotak deteksi
            thickness=2,
            text_thickness=2,
            text_scale=1
        )
        self.counts = {'mentah': 0, 'kurang matang': 0, 'matang': 0, 'terlalu matang': 0}  # Mendefinisikan atribut counts

    def process_image(self):
        result = self.model(self.image)[0]  # Melakukan deteksi objek pada gambar
        detections = sv.Detections.from_yolov8(result)  # Mengubah hasil deteksi menjadi objek Detections
        labels = [  # Membuat label untuk setiap deteksi
            f"{self.model.model.names[class_id]} {confidence:0.2f}"
            for _, confidence, class_id, _
            in detections]
        self.image = self.box_annotator.annotate(scene=self.image, detections=detections, labels=labels)  # Menggambar kotak deteksi dan label pada gambar
        cv2.imwrite(self.image_path, self.image)  # Menyimpan gambar yang telah diproses
        with open(self.image_path, "rb") as img_file:
            self.b64_string = base64.b64encode(img_file.read()).decode()

        # Hitung jumlah nanas pada setiap kategori
        counts = {'mentah': 0, 'kurang matang': 0, 'matang': 0, 'terlalu matang': 0}

        for _, confidence, class_id, _ in detections:
            category = self.model.model.names[class_id].lower()
            print("kategori yang terdeteksi = ", category)
            if category in self.counts:
                self.counts[category] += 1

        # Kirim data jumlah ke halaman HTML
        socketio.emit('update_counts', self.counts)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check')
def check():
    return render_template('check.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    img_data = request.form['img']
    img_data = base64.b64decode(img_data.split(',')[1])

    # Simpan gambar dengan timestamp sebagai nama file
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + '.png'
    file_path = 'images/' + filename
    with open(file_path, 'wb') as f:
        f.write(img_data)

    # Proses gambar dengan deteksi objek
    processor = ImageProcessor(file_path)
    processor.process_image()

    # Ubah file_path menjadi URL
    file_url = '/images/' + filename

    # Kirim data ke klien melalui Socket.IO
    socketio.emit('update', {"file_path": file_url, "img_data": processor.b64_string, "counts": processor.counts})

    return {"file_path": file_url, "img_data": processor.b64_string, "counts": processor.counts}

@app.route('/images/<filename>')
def send_image(filename):
    return send_from_directory('images', filename)

if __name__ == '__main__':
    socketio.run(app, debug=True)
