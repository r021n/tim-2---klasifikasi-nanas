Repository ini berisi kode Python untuk membuat aplikasi web sederhana. Aplikasi ini menggunakan Flask, sebuah microframework web Python yang populer.

Langkah-langkah penggunaan:

Buat environment Python
Untuk membuat environment Python, Anda dapat menggunakan perintah berikut:

python -m venv env
Perintah ini akan membuat folder baru bernama env di direktori saat ini. Folder ini berisi semua file yang diperlukan untuk menjalankan aplikasi Anda.

Install library Python
Untuk menginstal library Python yang diperlukan, Anda dapat menggunakan perintah berikut:

pip install -r requirements.txt
Perintah ini akan menginstal semua library Python yang tercantum dalam file requirements.txt.

Aktifkan environment
Untuk mengaktifkan environment Python, Anda dapat menggunakan perintah berikut:

source env/bin/activate
Perintah ini akan mengaktifkan environment Python bernama env.

Jalankan aplikasi
Untuk menjalankan aplikasi, Anda dapat menggunakan perintah berikut:

flask run
Perintah ini akan menjalankan aplikasi Anda di port 5000. Anda dapat mengakses aplikasi Anda di http://localhost:5000.

Contoh penggunaan:

Berikut adalah contoh penggunaan aplikasi ini:

# Buat environment Python
python -m venv env

# Aktifkan environment Python
source env/bin/activate

# Install library Python
pip install -r requirements.txt

# Jalankan aplikasi
flask run
Jika Anda mengikuti langkah-langkah di atas, Anda akan melihat pesan berikut di konsol:

* Serving Flask app "app" (lazy loading)
* Environment: production
* Debug mode: off
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
Sekarang, Anda dapat mengakses aplikasi Anda di http://localhost:5000.
