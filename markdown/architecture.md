# Architecture - Lab Equipment Loan System

## 1. Tujuan

Dokumen ini menjelaskan rancangan teknis backend **Lab Equipment Loan System** berdasarkan `requirement.md` dan `prd.md`.

Sistem menyediakan REST API untuk mengelola master alat laboratorium, transaksi peminjaman, pengembalian alat, serta riwayat peminjaman mahasiswa.

## 2. Teknologi

- **Bahasa:** Python 3.x
- **Backend framework:** Flask
- **Database:** SQLite
- **Format pertukaran data:** JSON
- **Antarmuka:** REST API

## 3. Gaya Arsitektur

Gunakan arsitektur berlapis sederhana (*layered architecture*) agar tanggung jawab setiap bagian terpisah tanpa menambah kompleksitas yang belum diperlukan.

Alur umum:

```text
HTTP Client
    |
    v
Flask Routes / Controllers
    |
    v
Service Layer (business rules)
    |
    v
Data Access Layer
    |
    v
SQLite Database
```

### Tanggung jawab lapisan

1. **Routes / Controllers**
   - Mendefinisikan endpoint dan HTTP method.
   - Membaca parameter, path, dan JSON request.
   - Memanggil service yang sesuai.
   - Mengubah hasil service menjadi respons JSON dan HTTP status code.
   - Tidak menyimpan aturan bisnis utama.

2. **Service Layer**
   - Menjalankan aturan peminjaman dan pengembalian.
   - Memvalidasi ketersediaan stok dan status transaksi.
   - Mengatur transaksi database agar perubahan stok dan transaksi konsisten.

3. **Data Access Layer**
   - Menangani query SQLite untuk entitas `Item` dan `Loan`.
   - Memisahkan operasi database dari route.
   - Menggunakan parameterized query, bukan menyusun SQL dari input pengguna.

4. **Database**
   - Menyimpan data master alat dan transaksi peminjaman.
   - Menegakkan primary key, foreign key, dan constraint dasar.

## 4. Struktur Direktori yang Disarankan

```text
lab-equipment-loan/
├── app/
│   ├── __init__.py
│   ├── routes/
│   │   ├── item_routes.py
│   │   └── loan_routes.py
│   ├── services/
│   │   ├── item_service.py
│   │   └── loan_service.py
│   ├── repositories/
│   │   ├── item_repository.py
│   │   └── loan_repository.py
│   ├── database.py
│   └── validators.py
├── instance/
│   └── lab_equipment.db
├── tests/
│   ├── test_items.py
│   └── test_loans.py
├── run.py
├── requirements.txt
├── requirement.md
├── prd.md
├── architecture.md
├── tasks.md
└── code_review.md
```

Struktur ini merupakan usulan pemisahan kode. Implementasi boleh disesuaikan selama tanggung jawab dan alur bisnis tetap terjaga.

## 5. Model Data

### 5.1 Item

| Kolom | Tipe | Aturan |
|---|---|---|
| `id` | INTEGER | Primary key |
| `name` | TEXT | Wajib diisi |
| `total_stock` | INTEGER | Jumlah stok keseluruhan |
| `available_stock` | INTEGER | Stok yang tersedia untuk dipinjam |

Ketentuan:
- `total_stock` dan `available_stock` harus berupa bilangan bulat non-negatif.
- Saat alat baru dibuat, `available_stock` diinisialisasi sama dengan `total_stock`.
- `available_stock` tidak boleh melebihi `total_stock`.

### 5.2 Loan

| Kolom | Tipe | Aturan |
|---|---|---|
| `id` | INTEGER | Primary key |
| `student_id` | TEXT | NIM mahasiswa, wajib diisi |
| `item_id` | INTEGER | Foreign key ke `Item.id` |
| `quantity` | INTEGER | Jumlah pinjaman, harus positif |
| `status` | TEXT | `BORROWED`, `RETURNED`, atau `CANCELLED` |
| `created_at` | TIMESTAMP | Waktu transaksi dibuat |

Ketentuan:
- `item_id` harus merujuk pada item yang tersedia.
- Status awal transaksi peminjaman adalah `BORROWED`.
- Pengembalian mengubah status menjadi `RETURNED`.
- Status `CANCELLED` tercantum dalam model data, tetapi alur pembatalannya belum didefinisikan dalam kebutuhan saat ini.

### 5.3 Relasi

```text
Item (1) -------- (N) Loan
  id                  item_id
```

Satu alat dapat memiliki banyak catatan transaksi peminjaman. Setiap transaksi peminjaman merujuk pada satu alat.

## 6. Rancangan API

Semua request dan response menggunakan JSON, kecuali endpoint GET yang tidak memerlukan body.

| Method | Endpoint | Fungsi | Respons sukses |
|---|---|---|---|
| GET | `/items` | Menampilkan daftar alat dan stok terkini | 200 OK |
| POST | `/items` | Menambahkan master alat | 201 Created |
| POST | `/loans` | Membuat transaksi peminjaman | 201 Created |
| PUT | `/loans/{id}/return` | Mengembalikan alat | 200 OK |
| GET | `/loans/student/{student_id}` | Melihat riwayat pinjaman mahasiswa | 200 OK |

### 6.1 Contoh request

**POST `/items`**

```json
{
  "name": "Multimeter",
  "total_stock": 10
}
```

`available_stock` diinisialisasi menjadi `10`.

**POST `/loans`**

```json
{
  "student_id": "20240001",
  "item_id": 1,
  "quantity": 2
}
```

**PUT `/loans/1/return`**

Tidak memerlukan body berdasarkan kebutuhan saat ini.

## 7. Alur Proses Bisnis

### 7.1 Menambahkan alat

1. Route menerima JSON.
2. Service memvalidasi `name` dan `total_stock`.
3. Sistem membuat data `Item`.
4. `available_stock` diisi sama dengan `total_stock`.
5. Sistem mengembalikan data alat dengan status `201 Created`.

### 7.2 Peminjaman alat

1. Route menerima `student_id`, `item_id`, dan `quantity`.
2. Service memvalidasi seluruh input dan memastikan `quantity` lebih besar dari nol.
3. Sistem memeriksa keberadaan item.
4. Sistem memeriksa apakah `available_stock` mencukupi.
5. Dalam satu transaksi database:
   - Kurangi `available_stock` sesuai `quantity`.
   - Buat data `Loan` dengan status `BORROWED`.
6. Jika salah satu operasi gagal, seluruh transaksi database dibatalkan (*rollback*).
7. Jika berhasil, kembalikan data transaksi dengan status `201 Created`.

### 7.3 Pengembalian alat

1. Route menerima ID transaksi.
2. Service mencari transaksi peminjaman.
3. Pastikan transaksi ditemukan dan statusnya belum `RETURNED`.
4. Dalam satu transaksi database:
   - Ubah status transaksi menjadi `RETURNED`.
   - Tambahkan `quantity` ke `available_stock` item terkait.
5. Jika salah satu operasi gagal, lakukan rollback.
6. Kembalikan data transaksi dengan status `200 OK`.

### 7.4 Riwayat peminjaman

1. Route menerima `student_id` dari URL.
2. Repository mengambil transaksi berdasarkan NIM.
3. Sistem mengembalikan daftar transaksi dalam format JSON.
4. Jika tidak ada transaksi, kembalikan daftar kosong dengan `200 OK`.

## 8. Konsistensi dan Integritas Data

- Aktifkan foreign key SQLite pada setiap koneksi (`PRAGMA foreign_keys = ON`).
- Gunakan transaksi database untuk operasi peminjaman dan pengembalian.
- Perubahan stok dan status transaksi harus berhasil atau gagal sebagai satu kesatuan.
- Gunakan query bersyarat saat mengurangi stok, misalnya hanya mengurangi jika `available_stock >= quantity`, untuk menghindari stok negatif.
- Hindari pengembalian ganda dengan memeriksa status transaksi di dalam transaksi database.
- Gunakan parameterized query.
- Simpan waktu transaksi secara konsisten. Format dan zona waktu dapat ditetapkan saat implementasi.

## 9. Validasi dan Penanganan Error

| Kondisi | HTTP status yang diharapkan |
|---|---|
| Input tidak valid atau field wajib tidak tersedia | 400 Bad Request |
| `item_id` tidak ditemukan saat peminjaman | 404 Not Found |
| Stok tidak mencukupi | 400 Bad Request |
| Transaksi pinjaman tidak ditemukan saat pengembalian | 404 Not Found |
| Transaksi sudah `RETURNED` | 400 Bad Request |
| Operasi berhasil membuat item/peminjaman | 201 Created |
| Operasi GET atau pengembalian berhasil | 200 OK |

Gunakan format respons error yang konsisten, misalnya:

```json
{
  "error": "Insufficient stock"
}
```

Pesan error harus informatif dan tidak membocorkan detail internal database.

## 10. Batasan dan Hal yang Belum Ditentukan

Hal berikut belum dijelaskan dalam requirement dan PRD. Jangan menganggapnya sebagai fitur wajib tanpa keputusan lanjutan:

- Autentikasi dan otorisasi Petugas Lab/Mahasiswa.
- Endpoint untuk mengubah atau menghapus master alat.
- Proses pembatalan transaksi (`CANCELLED`).
- Batas maksimum jumlah pinjaman.
- Tanggal jatuh tempo dan denda keterlambatan.
- Pagination, pencarian, dan pengurutan data.
- Format detail respons JSON di luar kriteria yang telah ditentukan.
- Strategi deployment dan konfigurasi production.

Implementasi awal sebaiknya berfokus pada endpoint dan aturan bisnis yang sudah ditetapkan.
