# 📊 Automated Data Validator

Aplikasi web interaktif (*web app*) berbasis Python dan Streamlit untuk memfilter, mencocokkan, serta mentransformasi data peserta webinar secara dinamis. Tools ini dirancang untuk memudahkan penyiapan data siap pakai sebelum diunggah ke sistem *email marketing* atau *campaign distribution*.

---

## ✨ Fitur Utama

- **Flexibility File Input:** Mendukung format `.csv` dan `.xlsx` (Excel) untuk data peserta lengkap maupun daftar email penyaring.
- **Dynamic Header Mapping:** Pengguna dapat memilih kolom `Email` dan `Nama` secara fleksibel menyesuaikan variabel header tiap file.
- **Custom JSON Attributes:** Fitur opsional untuk menggabungkan kolom-kolom informasi tambahan (misal: Nomor WhatsApp, Instansi, URL Sertifikat) menjadi format objek JSON `attributes`.
- **Preservasi Format Nomor HP:** Membaca nomor telepon sebagai tipe teks (*string*) sehingga digit angka `0` di depan tidak hilang saat diproses.
- **Custom Output Filename:** Nama file hasil ekstraksi dapat disesuaikan sebelum diunduh (format `.csv` dengan pengodean `utf-8-sig` yang aman untuk Microsoft Excel).
- **Multi-User Ready:** Siap di-deploy ke cloud agar dapat diakses oleh tim tanpa perlu instalasi lingkungan Python lokal.

---

## 🛠️ Struktur Proyek

```text
webinar-data-processor/
│
├── app.py              # Logika utama aplikasi Streamlit
├── requirements.txt    # Daftar pustaka / dependensi Python
└── README.md           # Dokumentasi proyek
