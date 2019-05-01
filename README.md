# Repositori Pemilu 2019

# Fungsi (sampai saat ini)
Mengambil data atau metadata dari KPU untuk ditabulasi dan menghasilkan tabulasi sesuai yang ada di KPU.
Mengambil gambar C1 dari tabulasi yang sudah diambil sebelumnya.
Belum ada pencocokan data antara data yang diinput dengan gambar yang dipindai dan diunggah ke tempat yang sama.

Terinspirasi dari https://github.com/seuriously/pilpres2019

# Daftar yang Akan Dikerjakan
- ~~Konkurensi untuk mempercepat pengambilan data (sekarang masih terbatas di jumlah kelurahan)~~
- ~~Manipulasi koneksi supaya bisa mengambil semua data tanpa gangguan~~ (Asumsi sudah optimal, bisa cek kode untuk optimal di mesin dan koneksi Anda)
- ~~Sistem antrian ketika server KPU tidak bisa diakses di waktu-waktu tertentu~~
- ~~Pengambilan gambar C1~~
- ~~Konkurensi untuk mempercepat pengambilan gambar C1~~
- Penggunaan Pemelajaran Mesin untuk mengenali karakter pada gambar C1 (yang ini bakal paling wacana, langkahnya panjang soalnya)

# Cara Penggunaan
- Pengambilan metadata :
  `python3 crawl_metadata.py`
- Pengambilan data :
  `python3 crawl_tps.py [file hasil pengambilan metadata] [file hasil pengambilan data sebelumnya (jika ada)] 2>[file output tempat data tps yang gagal diambil]` (tanda [] hanya untuk kejelasan)
- Pengambilan gambar C1 :
  `python3 crawl_images.py [file hasil pengambilan data] [folder output] 2>[file output tempat link gambar yang gagal diambil]` (tanda [] hanya untuk kejelasan)

# Fun Fact
- KPU memperbaharui hasil TPS setiap 15 menit, bukan 30 menit, apalagi per hari