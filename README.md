 Penerapan Struktur Data Python (List, Tuple, dan Dictionary)

Pada praktikum ini dilakukan tiga percobaan sederhana untuk memahami penggunaan struktur data dasar Python yang sering digunakan dalam pemrograman grafika komputer, yaitu list, tuple, dan dictionary.

![List](https://github.com/user-attachments/assets/38629cb9-7232-4786-b88c-ccc475f539f2)
Gambar pertama menunjukkan hasil dari percobaan menggunakan list. Pada program ini dibuat sebuah list berisi tiga pasangan titik koordinat, yaitu [(0, 0), (50, 50), (100, 0)]. 
Setiap elemen di dalam list merupakan pasangan titik (x, y). Program kemudian menampilkan seluruh titik tersebut menggunakan perulangan for, sehingga setiap pasangan koordinat
ditampilkan satu per satu di layar. Percobaan ini menunjukkan bahwa list dapat digunakan untuk menyimpan banyak nilai berurutan, seperti kumpulan titik pada garis atau poligon 
dalam grafika komputer.

![Tuple](https://github.com/user-attachments/assets/f6961872-ab80-43c9-8d07-a1ed8a007c08)
Gambar kedua merupakan hasil dari percobaan kedua, yaitu penggunaan tuple. Pada program ini dibuat sebuah tuple bernama `pusat` yang berisi satu titik `(0, 0)`. Berbeda dengan 
list, tuple bersifat tetap (immutable), sehingga nilainya tidak dapat diubah setelah dibuat. Program kemudian menampilkan nilai tuple tersebut ke layar.
Percobaan ini memperlihatkan bahwa tuple cocok digunakan untuk menyimpan data yang tidak perlu diubah, misalnya titik pusat rotasi dalam bidang grafika.

![Dictionary](https://github.com/user-attachments/assets/1c4f10cc-d27d-41b7-8c11-e79a06111bc6)
Percobaan ketiga menggunakan dictionary dengan atribut objek berupa koordinat dan warna, yaitu {"x": 10, "y": 20, "warna": "biru"}. Program menampilkan 
hasilnya dalam format teks: Titik (10,20) berwarna biru. Percobaan ini menunjukkan bahwa *dictionary* sangat berguna untuk menyimpan data dalam bentuk 
pasangan key-value, seperti atribut posisi, warna, dan ukuran pada objek grafika.

Secara keseluruhan, ketiga percobaan ini memberikan pemahaman dasar bahwa list, tuple, dan dictionary memiliki peran penting dalam pengelolaan data koordinat dan atribut
objek pada grafika komputer. List digunakan untuk menyimpan kumpulan titik yang dapat berubah, tuple untuk titik tetap, dan dictionary untuk menyimpan atribut terstruktur
dari suatu objek.

# 🧩 Penerapan Struktur Data Python (List, Tuple, dan Dictionary)

Pada praktikum ini dilakukan tiga percobaan sederhana untuk memahami penggunaan **struktur data dasar Python** yang sering digunakan dalam **pemrograman grafika komputer**, yaitu **List**, **Tuple**, dan **Dictionary**.

---

## 🔹 1. List — Menyimpan Kumpulan Titik

![List](https://github.com/user-attachments/assets/38629cb9-7232-4786-b88c-ccc475f539f2)

Gambar pertama menunjukkan hasil dari percobaan menggunakan **List**.  
Pada program ini dibuat sebuah list berisi tiga pasangan titik koordinat:
```python
[(0, 0), (50, 50), (100, 0)]


