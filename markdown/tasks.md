# Development Tasks - Lab Equipment Loan System

## Petunjuk

- Kerjakan tugas secara berurutan.
- Tandai `[x]` setelah tugas selesai dan sudah diperiksa.
- Gunakan `requirement.md`, `prd.md`, dan `architecture.md` sebagai acuan.
- Jangan menambahkan fitur di luar kebutuhan tanpa persetujuan.
- Pastikan setiap endpoint dapat diuji menggunakan HTTP client seperti Postman.

## 1. Project Setup

- [x] Buat struktur direktori proyek sesuai `architecture.md`.
- [x] Siapkan virtual environment Python.
- [x] Buat `requirements.txt` dan tambahkan Flask.
- [x] Buat entry point aplikasi (`run.py`).
- [x] Buat konfigurasi dasar aplikasi Flask.
- [x] Pastikan aplikasi dapat dijalankan secara lokal.

## 2. Database

- [x] Buat modul koneksi database SQLite.
- [x] Buat inisialisasi tabel `Item`.
- [x] Buat inisialisasi tabel `Loan`.
- [x] Definisikan primary key dan foreign key.
- [x] Aktifkan foreign key SQLite pada setiap koneksi.
- [x] Tambahkan constraint dasar untuk stok, quantity, dan status.
- [x] Pastikan database dan tabel dapat dibuat tanpa error.

## 3. Data Access Layer

- [x] Buat repository untuk entitas `Item`.
- [x] Implementasikan penyimpanan item baru.
- [x] Implementasikan pengambilan seluruh item.
- [x] Implementasikan pengambilan item berdasarkan ID.
- [x] Implementasikan pengurangan stok secara bersyarat.
- [x] Implementasikan penambahan stok.
- [x] Buat repository untuk entitas `Loan`.
- [x] Implementasikan pembuatan transaksi pinjaman.
- [x] Implementasikan pencarian transaksi berdasarkan ID.
- [x] Implementasikan pembaruan status transaksi.
- [x] Implementasikan pengambilan riwayat berdasarkan NIM.
- [x] Gunakan parameterized query pada seluruh query yang menerima input.

## 4. Service Layer dan Business Logic

### 4.1 Item Service

- [ ] Validasi nama alat wajib diisi.
- [ ] Validasi `total_stock` berupa bilangan bulat non-negatif.
- [ ] Inisialisasi `available_stock` sama dengan `total_stock`.
- [ ] Implementasikan layanan untuk menampilkan daftar alat.
- [ ] Implementasikan layanan untuk menambahkan alat.

### 4.2 Loan Service

- [ ] Validasi `student_id`, `item_id`, dan `quantity`.
- [ ] Pastikan `quantity` berupa bilangan bulat positif.
- [ ] Pastikan item tersedia di database.
- [ ] Tolak peminjaman jika stok tidak mencukupi.
- [ ] Kurangi stok dan buat transaksi `BORROWED` dalam satu transaksi database.
- [ ] Lakukan rollback jika proses peminjaman gagal.
- [ ] Pastikan transaksi pengembalian ditemukan.
- [ ] Tolak pengembalian jika status sudah `RETURNED`.
- [ ] Ubah status menjadi `RETURNED` dan pulihkan stok dalam satu transaksi database.
- [ ] Lakukan rollback jika proses pengembalian gagal.
- [ ] Implementasikan pengambilan riwayat peminjaman berdasarkan NIM.

## 5. API Routes

- [ ] Implementasikan `GET /items`.
- [ ] Implementasikan `POST /items`.
- [ ] Implementasikan `POST /loans`.
- [ ] Implementasikan `PUT /loans/{id}/return`.
- [ ] Implementasikan `GET /loans/student/{student_id}`.
- [ ] Pastikan seluruh endpoint menerima atau mengembalikan JSON sesuai kebutuhan.
- [ ] Pastikan HTTP status code sesuai acceptance criteria.
- [ ] Gunakan format respons sukses dan error yang konsisten.

## 6. Testing

### 6.1 Item API

- [ ] Uji `GET /items` ketika database kosong.
- [ ] Uji penambahan item dengan data valid.
- [ ] Uji penambahan item tanpa nama.
- [ ] Uji penambahan item dengan stok negatif.
- [ ] Uji bahwa stok awal tersedia sama dengan stok total.

### 6.2 Loan API

- [ ] Uji peminjaman dengan data valid.
- [ ] Uji peminjaman ketika stok mencukupi.
- [ ] Uji peminjaman ketika quantity melebihi stok.
- [ ] Uji peminjaman dengan `item_id` yang tidak ditemukan.
- [ ] Uji peminjaman dengan quantity nol atau negatif.
- [ ] Pastikan stok berkurang sesuai jumlah pinjaman.
- [ ] Pastikan transaksi gagal tidak mengubah stok.

### 6.3 Return API

- [ ] Uji pengembalian transaksi yang valid.
- [ ] Pastikan status berubah menjadi `RETURNED`.
- [ ] Pastikan stok bertambah sesuai quantity transaksi.
- [ ] Uji pengembalian transaksi yang tidak ditemukan.
- [ ] Uji pengembalian transaksi yang sudah `RETURNED`.
- [ ] Pastikan pengembalian ganda tidak menambah stok.

### 6.4 Student Loan History API

- [ ] Uji riwayat dengan NIM yang memiliki transaksi.
- [ ] Uji riwayat dengan NIM yang belum memiliki transaksi.
- [ ] Pastikan hasil hanya memuat transaksi milik NIM yang diminta.

## 7. Final Verification

- [ ] Jalankan seluruh pengujian.
- [ ] Periksa konsistensi stok setelah beberapa transaksi peminjaman dan pengembalian.
- [ ] Periksa seluruh endpoint menggunakan Postman.
- [ ] Pastikan tidak ada error yang belum ditangani.
- [ ] Periksa struktur proyek dan hapus kode yang tidak digunakan.
- [ ] Perbarui dokumentasi cara instalasi dan menjalankan aplikasi.
- [ ] Pastikan implementasi sesuai dengan `requirement.md`, `prd.md`, dan `architecture.md`.

## 8. Definition of Done

Pekerjaan dianggap selesai apabila:

1. Kelima endpoint yang ditentukan telah tersedia.
2. Semua acceptance criteria dalam `prd.md` terpenuhi.
3. Stok tidak pernah menjadi negatif akibat transaksi peminjaman.
4. Pengembalian tidak dapat diproses lebih dari satu kali untuk transaksi yang sama.
5. Perubahan stok dan transaksi dilakukan secara atomik.
6. Pengujian utama berhasil dan endpoint dapat diuji melalui Postman.
7. Dokumentasi dasar penggunaan aplikasi tersedia.
