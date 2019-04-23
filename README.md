# Repositori Pemilu 2019

# Fungsi (sampai saat ini)
Mengambil data dari KPU untuk ditabulasi dan menghasilkan tabulasi sesuai yang ada di KPU.
Mengambil gambar C1 dari tabulasi yang sudah diambil sebelumnya.
Belum ada pencocokan data antara data yang diinput dengan gambar yang dipindai dan diunggah ke tempat yang sama.

Terinspirasi dari https://github.com/seuriously/pilpres2019

# Daftar yang Akan Dikerjakan
- Konkurensi untuk mempercepat pengambilan data (sekarang masih terbatas di jumlah kelurahan)
- Sistem antrian ketika server KPU tidak bisa diakses di waktu-waktu tertentu
- Konkurensi untuk mempercepat pengambilan gambar C1
- Penggunaan Pemelajaran Mesin untuk mengenali karakter pada gambar C1 (yang ini bakal paling wacana, langkahnya panjang soalnya)

# Cara Penggunaan
- Pengambilan data :
  `python3 crawl.py`
- Pengambilan gambar C1 :
  `python3 crawl_images.py <file hasil pengambilan data>`

# Fun Fact
- Server KPU tidak bisa diakses pada jam 00.00 WIB, jadi disarankan tidak crawling pada jam tersebut