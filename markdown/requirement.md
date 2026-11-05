# Software Requirement Specification (SRS) - Lab Equipment Loan System ## 1. Overview Sistem
Informasi backend untuk mengelola peminjaman alat/fasilitas laboratorium kampus oleh mahasiswa deng
an kontrol stok otomatis dan verifikasi status peminjaman. ## 2. Tech Stack & Environment - Languag
e: Python 3.x - Framework: Flask - Database: SQLite (Relational DB) - Data Interchange: J
SON ## 3. Data Model & Database Schema 1. Item (Alat Lab): - id (Integer, Primary Key) - name (Stri
ng, Required) - total_stock (Integer) - available_stock (Integer) 2. Loan (Transaksi Peminjaman): -
id (Integer, Primary Key) - student_id (String, NIM Mahasiswa) - item_id (Integer, Foreign Key -> I
tem.id) - quantity (Integer) - status (String: BORROWED, RETURNED, CANCELLED) - created_at (Timesta
mp) ## 4. API Endpoints - GET /items : Menampilkan daftar alat dan ketersediaan stok. - POST /items
: Menambah master data alat baru. - POST /loans : Mengajukan peminjaman alat (mengurangi available_
stock). - PUT /loans/{id}/return : Mengembalikan alat yang dipinjam (menambah kembali available_sto
ck). - GET /loans/student/{student_id} : Menampilkan riwayat peminjaman berdasarkan NIM.