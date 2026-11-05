# Code Review Checklist - Lab Equipment Loan System

## 1. Tujuan Review

Dokumen ini digunakan untuk memeriksa kualitas implementasi backend Lab Equipment Loan System agar sesuai dengan `requirement.md`, `prd.md`, dan `architecture.md`.

Review berfokus pada kesesuaian fungsi, aturan bisnis, integritas stok, konsistensi database, kualitas API, dan keterbacaan kode.

## 2. Requirement Compliance

- [ ] Implementasi menggunakan Python 3.x.
- [ ] Backend menggunakan Flask.
- [ ] Database menggunakan SQLite.
- [ ] Pertukaran data API menggunakan JSON.
- [ ] Seluruh endpoint yang ditentukan tersedia:
  - [ ] `GET /items`
  - [ ] `POST /items`
  - [ ] `POST /loans`
  - [ ] `PUT /loans/{id}/return`
  - [ ] `GET /loans/student/{student_id}`
- [ ] Nama field dan status transaksi sesuai spesifikasi.

## 3. Data Model dan Database

- [ ] Tabel `Item` memiliki `id`, `name`, `total_stock`, dan `available_stock`.
- [ ] Tabel `Loan` memiliki `id`, `student_id`, `item_id`, `quantity`, `status`, dan `created_at`.
- [ ] Primary key dan foreign key didefinisikan dengan benar.
- [ ] Foreign key SQLite diaktifkan pada setiap koneksi.
- [ ] Stok tidak menerima nilai negatif.
- [ ] `quantity` transaksi harus lebih besar dari nol.
- [ ] Status transaksi hanya menggunakan nilai yang diizinkan.
- [ ] `available_stock` tidak melebihi `total_stock`.
- [ ] Query yang menerima input menggunakan parameterized query.
- [ ] Koneksi database ditutup atau dikelola dengan benar.

## 4. Business Logic

### 4.1 Penambahan Item

- [ ] Field `name` wajib diisi.
- [ ] `total_stock` divalidasi sebagai bilangan bulat non-negatif.
- [ ] `available_stock` otomatis diinisialisasi sama dengan `total_stock`.
- [ ] Data tidak tersimpan jika validasi gagal.

### 4.2 Peminjaman

- [ ] `student_id`, `item_id`, dan `quantity` divalidasi.
- [ ] `quantity` harus berupa bilangan bulat positif.
- [ ] Sistem memeriksa keberadaan item.
- [ ] Sistem menolak peminjaman jika stok tidak mencukupi.
- [ ] Sistem mengembalikan `404 Not Found` jika item tidak ditemukan.
- [ ] Sistem mengembalikan `400 Bad Request` jika stok tidak mencukupi.
- [ ] Sistem mengembalikan `201 Created` jika peminjaman berhasil.
- [ ] Stok berkurang tepat sesuai quantity.
- [ ] Status awal transaksi adalah `BORROWED`.
- [ ] Pembuatan transaksi dan pengurangan stok dilakukan secara atomik.
- [ ] Kegagalan salah satu operasi menyebabkan rollback.

### 4.3 Pengembalian

- [ ] Sistem memeriksa keberadaan transaksi.
- [ ] Sistem menolak transaksi yang sudah berstatus `RETURNED`.
- [ ] Sistem mengembalikan `400 Bad Request` untuk pengembalian ulang.
- [ ] Sistem mengembalikan `404 Not Found` jika transaksi tidak ditemukan.
- [ ] Status transaksi berubah menjadi `RETURNED`.
- [ ] Stok bertambah sesuai quantity transaksi.
- [ ] Pembaruan status dan pemulihan stok dilakukan secara atomik.
- [ ] Pengembalian ulang tidak menyebabkan stok bertambah dua kali.

### 4.4 Riwayat Peminjaman

- [ ] Hasil pencarian difilter berdasarkan `student_id`.
- [ ] Data mahasiswa lain tidak ikut ditampilkan.
- [ ] Jika tidak ada transaksi, API mengembalikan daftar kosong secara konsisten.

## 5. API Contract dan HTTP Response

- [ ] Endpoint menggunakan HTTP method dan path yang benar.
- [ ] Request body menggunakan JSON untuk endpoint yang memerlukannya.
- [ ] Response menggunakan JSON dengan struktur konsisten.
- [ ] HTTP status code sesuai kondisi.
- [ ] Error response memberikan pesan yang jelas.
- [ ] Error tidak membocorkan SQL, stack trace, atau informasi internal.
- [ ] Respons GET `/items` menampilkan stok terkini dari database.
- [ ] Tidak ada nilai stok yang hanya diperbarui di memori tanpa disimpan ke database.

## 6. Code Quality

- [ ] Route/controller tidak menampung seluruh business logic.
- [ ] Aturan bisnis ditempatkan pada service layer.
- [ ] Operasi query ditempatkan pada repository/data access layer.
- [ ] Fungsi memiliki tanggung jawab yang jelas.
- [ ] Nama variabel, fungsi, dan modul mudah dipahami.
- [ ] Tidak ada duplikasi logika validasi atau transaksi yang tidak perlu.
- [ ] Tidak ada hard-coded path database yang menyulitkan konfigurasi.
- [ ] Tidak ada kode mati, debug print, atau TODO yang tidak dijelaskan.
- [ ] Dependency tercatat di `requirements.txt`.
- [ ] Aplikasi dapat dijalankan mengikuti dokumentasi.

## 7. Security dan Reliability

- [ ] Input pengguna divalidasi di sisi backend.
- [ ] SQL injection dicegah dengan parameterized query.
- [ ] Error internal tidak dikirimkan secara mentah kepada client.
- [ ] Transaksi database digunakan untuk menjaga konsistensi stok.
- [ ] Operasi pengurangan stok bersyarat agar stok tidak menjadi negatif.
- [ ] Pengembalian ganda dicegah melalui pemeriksaan status dalam transaksi.
- [ ] Tidak ada kredensial atau secret yang disimpan di source code.

Catatan: autentikasi dan otorisasi belum ditetapkan dalam requirement/PRD. Ketiadaannya tidak otomatis dianggap sebagai kegagalan implementasi terhadap ruang lingkup saat ini, tetapi perlu dicatat sebagai batasan sebelum sistem digunakan di lingkungan nyata.

## 8. Test Evidence

- [ ] Ada bukti pengujian untuk setiap endpoint.
- [ ] Ada pengujian input valid dan tidak valid.
- [ ] Ada pengujian stok tidak mencukupi.
- [ ] Ada pengujian item dan transaksi yang tidak ditemukan.
- [ ] Ada pengujian pengembalian ganda.
- [ ] Ada pengujian bahwa stok tetap konsisten ketika transaksi gagal.
- [ ] Hasil pengujian dapat diulang dengan langkah yang jelas.

## 9. Review Findings

Catat temuan review dengan format berikut:

| ID | File/Bagian | Temuan | Tingkat | Rekomendasi | Status |
|---|---|---|---|---|---|
| CR-01 | - | - | - | - | Open |

Gunakan tingkat prioritas:

- **Critical:** menyebabkan kehilangan/kerusakan data, stok tidak konsisten, atau celah keamanan serius.
- **High:** aturan bisnis utama tidak berjalan atau endpoint utama gagal.
- **Medium:** validasi, respons API, atau kualitas kode bermasalah tetapi dampaknya terbatas.
- **Low:** masalah keterbacaan, konsistensi, atau perbaikan kecil.

## 10. Review Summary

Isi setelah proses review:

- **Status:** Pending / Approved / Approved with Changes / Rejected
- **Jumlah temuan Critical:**
- **Jumlah temuan High:**
- **Jumlah temuan Medium:**
- **Jumlah temuan Low:**
- **Catatan reviewer:**

Kode hanya layak disetujui apabila seluruh alur utama berjalan, acceptance criteria terpenuhi, dan tidak ada temuan Critical atau High yang belum diselesaikan.
