
Mini Scene 2D – Simulasi Lingkungan Siang dan Malam Berbasis Grafika Komputer menggunakan Python Turtle.

**Konsep Grafika yang Digunakan**
Proyek ini menampilkan sebuah adegan 2D berupa lingkungan alam yang realistis, meliputi gunung, danau dengan refleksi, rumah, jalan, pohon, awan, burung, matahari, bulan, bintang, dan lampu jalan. Adegan disimulasikan secara dinamis dengan konsep **animasi frame-by-frame**, **pergantian siang dan malam**, serta **efek refleksi objek pada permukaan air**. Transformasi geometris seperti translasi, rotasi, skala, dan refleksi diterapkan untuk menciptakan kesan gerak dan kedalaman visual.

**Algoritma yang Dipakai**
Program ini menggunakan beberapa algoritma dasar grafika komputer, yaitu **Algoritma DDA (Digital Differential Analyzer)** untuk menggambar garis (jalan, sinar matahari, batang pohon, rumput, burung).

**Algoritma Midpoint Circle** untuk menggambar matahari.
**Transformasi geometri 2D** (translasi untuk pergerakan matahari, bulan, awan, dan burung; rotasi untuk sinar matahari; skala untuk animasi awan; serta refleksi untuk pantulan objek di air). Selain itu, digunakan logika **state machine** untuk mengatur pergantian mode langit (siang, malam, dan jeda kosong).

**Cara Menjalankan Program**
Pastikan Python sudah terinstal di komputer. Simpan seluruh file gambar (cloud_small.gif, cloud_medium.gif, cloud_large.gif, dan bulan.gif) dalam satu folder yang sama dengan file program Python. Jalankan program menggunakan editor seperti **Thonny**, **IDLE**, atau melalui terminal dengan perintah `python nama_file.py`. Setelah dijalankan, animasi akan berjalan otomatis menampilkan siklus siang dan malam secara terus-menerus.

