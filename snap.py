from ultralytics import YOLO  # Mengimpor kelas YOLO dari pustaka ultralytics

def detect_objects_on_image(buf):
    model = YOLO("model\Best_600_epoch.pt")  # Membuat objek model YOLO dengan model yang diberikan
    results = model.predict(buf)  # Memprediksi objek pada gambar menggunakan model YOLO
    result = results[0]  # Mengambil hasil prediksi untuk gambar pertama
    output = []
    for box in result.boxes:
        x1, y1, x2, y2 = [
            round(x) for x in box.xyxy[0].tolist()
        ]
        class_id = box.cls[0].item()
        prob = round(box.conf[0].item(), 2)
        output.append([
            x1, y1, x2, y2, result.names[class_id], prob
        ])
    return output
