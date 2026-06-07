# SPK Pemilihan Laptop - Metode SAW

Aplikasi Sistem Pendukung Keputusan (SPK) untuk membantu pemilihan laptop menggunakan metode Simple Additive Weighting (SAW).

## Fitur

- **Rekomendasi Cerdas**: Mengonversi kebutuhan pengguna (tujuan, budget, mobilitas, multitasking) menjadi bobot kriteria secara otomatis.
- **Perhitungan SAW Transparan**: Menampilkan matriks normalisasi dan detail perhitungan nilai preferensi.
- **Dashboard Admin**: CRUD data laptop dan kriteria, serta statistik penggunaan.
- **Riwayat Rekomendasi**: Menyimpan hasil pencarian sebelumnya.
- **UI Modern**: Menggunakan Bootstrap 5 dengan fitur Dark Mode.

## Instalasi

1. Pastikan Python sudah terinstal.
2. Instal dependensi:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi:
   ```bash
   python app.py
   ```
4. Buka browser dan akses `http://127.0.0.1:5000`.

## Struktur Proyek

- `app.py`: Entry point aplikasi.
- `models.py`: Definisi database (SQLAlchemy).
- `saw.py`: Logika perhitungan metode SAW.
- `routes/`: Blueprint untuk routing user dan admin.
- `templates/`: File HTML Jinja2.
- `static/`: Aset CSS/JS (opsional).
