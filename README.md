# Sistem Rekomendasi Laptop Terbaik - Metode SAW

Sistem Pendukung Keputusan (SPK) untuk merekomendasikan laptop terbaik berdasarkan kriteria pengguna menggunakan metode **Simple Additive Weighting (SAW)**.

## Fitur Utama

- **Sistem Autentikasi**: Login dan Register (Role User dan Admin).
- **Rekomendasi Laptop (SAW)**: Memberikan rekomendasi laptop berdasarkan input pengguna (bobot prioritas untuk Harga, RAM, Storage, CPU, dan GPU).
- **Riwayat Rekomendasi**: Pengguna dapat melihat riwayat rekomendasi yang pernah dilakukan.
- **Admin Dashboard**: Admin dapat mengelola data laptop, kriteria, dan melihat log aktivitas pengguna.
- **Dark Mode**: Dukungan mode gelap untuk kenyamanan pengguna.
- **Desain Modern**: Menggunakan Bootstrap 5 untuk antarmuka yang responsif dan estetis.

## Teknologi yang Digunakan

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: SQLite
- **Metode SPK**: Simple Additive Weighting (SAW)

## Instalasi dan Menjalankan Proyek

1. **Clone repositori ini**:
   ```bash
   git clone https://github.com/zyxx123/Sistem-rekomendasi-laptop-terbaik.git
   cd Sistem-rekomendasi-laptop-terbaik
   ```

2. **Buat Virtual Environment (Opsional namun direkomendasikan)**:
   ```bash
   python -m venv venv
   # Di Windows
   venv\Scripts\activate
   # Di Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Inisialisasi Database** (jika belum ada):
   - Database SQLite akan otomatis dibuat dan diisi data awal (*seed data*) saat aplikasi dijalankan pertama kali.

5. **Jalankan aplikasi**:
   ```bash
   flask run
   # atau
   python app.py
   ```

6. **Akses di Browser**:
   Buka `http://127.0.0.1:5001` (atau port sesuai yang dikonfigurasi).

## Penggunaan

1. **User Biasa**: Daftar akun baru atau login, kemudian masuk ke halaman **Rekomendasi**, masukkan nilai prioritas untuk masing-masing kriteria (skala 1-5), lalu klik **Hitung Rekomendasi**.
2. **Admin**: Login dengan akun admin (buat melalui database atau role admin yang tersedia) untuk mengakses **Admin Dashboard** dan mengelola dataset laptop.
