# Lab Equipment Loan System

Backend REST API untuk mengelola peminjaman alat laboratorium kampus, lengkap dengan kontrol stok otomatis dan verifikasi status transaksi.

## Teknologi

- Python 3.x
- Flask
- SQLite
- JSON

## Struktur Proyek

```text
opencode/
├── app/
│   ├── __init__.py          # Application factory, blueprint, error handler
│   ├── database.py          # Koneksi SQLite dan CLI init-db
│   ├── errors.py            # ApiError
│   ├── schema.sql           # Skema tabel items dan loans
│   ├── validators.py        # Validasi input
│   ├── routes/
│   │   ├── item_routes.py
│   │   └── loan_routes.py
│   ├── services/
│   │   ├── item_service.py
│   │   └── loan_service.py
│   └── repositories/
│       ├── item_repository.py
│       └── loan_repository.py
├── instance/                # Database SQLite (tidak di-commit)
├── markdown/                # Dokumentasi proyek
├── tests/
│   ├── base.py
│   ├── test_items.py
│   └── test_loans.py
├── requirements.txt
└── run.py
```

## Instalasi

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Untuk Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Inisialisasi Database

```powershell
.\.venv\Scripts\python.exe -m flask --app run:app init-db
```

Perintah ini membuat `instance/lab_equipment.db` beserta tabel `items` dan `loans`. Perintah aman dijalankan ulang karena memakai `CREATE TABLE IF NOT EXISTS`.

## Menjalankan Aplikasi

```powershell
.\.venv\Scripts\python.exe run.py
```

Server berjalan di `http://127.0.0.1:5000`.

## Endpoint

| Method | Endpoint | Fungsi | Status sukses |
|---|---|---|---|
| GET | `/items` | Daftar alat dan stok terkini | 200 |
| POST | `/items` | Tambah master alat | 201 |
| POST | `/loans` | Ajukan peminjaman | 201 |
| PUT | `/loans/{id}/return` | Kembalikan alat | 200 |
| GET | `/loans/student/{student_id}` | Riwayat pinjaman mahasiswa | 200 |

### Contoh Penggunaan

Tambah alat:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/items `
  -ContentType "application/json" `
  -Body '{"name":"Multimeter","total_stock":10}'
```

Ajukan peminjaman:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/loans `
  -ContentType "application/json" `
  -Body '{"student_id":"20240001","item_id":1,"quantity":2}'
```

Kembalikan alat:

```powershell
Invoke-RestMethod -Method Put -Uri http://127.0.0.1:5000/loans/1/return
```

Riwayat mahasiswa:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/loans/student/20240001
```

### Format Error

Semua error dikembalikan sebagai JSON:

```json
{
  "error": "Insufficient stock"
}
```

## Menjalankan Pengujian

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Pengujian menggunakan database sementara sehingga tidak mengubah database lokal.

## Aturan Bisnis

- Stok berkurang otomatis saat peminjaman berhasil dicatat.
- Peminjaman ditolak dengan `400 Bad Request` jika stok tidak mencukupi.
- `item_id` yang tidak ada menghasilkan `404 Not Found`.
- Pengembalian mengubah status menjadi `RETURNED` dan memulihkan stok.
- Transaksi yang sudah `RETURNED` tidak dapat dikembalikan lagi (`400 Bad Request`).
- Perubahan stok dan transaksi dilakukan secara atomik dengan rollback saat gagal.
- Stok tidak pernah menjadi negatif.

## Batasan

Fitur berikut belum termasuk dalam ruang lingkup saat ini:

- Autentikasi dan otorisasi.
- Endpoint ubah/hapus master alat.
- Alur pembatalan transaksi (`CANCELLED`).
- Jatuh tempo dan denda.
- Pagination, pencarian, dan pengurutan.
- Konfigurasi deployment production.
