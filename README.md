
Dalam grafika komputer, menggambar objek geometri pada layar (rasterisasi) dilakukan dengan menentukan serangkaian piksel diskrit. Garis digambar menggunakan Algoritma Bresenham, yang merupakan metode efisien karena hanya menggunakan aritmatika integer (tanpa bilangan desimal) untuk menentukan jalur piksel terdekat antara dua titik $(x_1, y_1)$ dan $(x_2, y_2)$. Inti dari algoritma ini adalah variabel keputusan ($p$) yang mengukur seberapa jauh garis ideal dari dua pilihan piksel yang mungkin. Variabel ini diperbarui dalam setiap langkah horizontal, yang kemudian menentukan apakah piksel berikutnya harus bergerak satu langkah vertikal ($y \pm 1$) atau tetap berada pada level $y$ yang sama.


<img width="300" height="300" alt="image" src="https://github.com/user-attachments/assets/bb6eda83-4f76-4d52-876b-07eafc06d93b" />



Sementara itu, Lingkaran digambar menggunakan Algoritma Midpoint Circle yang sangat memanfaatkan simetri delapan arah (oktan) dari lingkaran.  Algoritma ini hanya perlu menghitung titik-titik diskrit untuk seperdelapan lingkaran (misalnya, dari $x=0$ hingga $x=y$) dimulai dari $(0, r)$. Sama seperti Bresenham, ia menggunakan variabel keputusan ($p$) untuk memilih piksel mana yang paling mendekati busur lingkaran ideal dalam setiap langkah penambahan $x$. Setelah satu titik dihitung, tujuh titik simetris lainnya langsung dipetakan, menyelesaikan seluruh lingkaran dengan perhitungan minimal.
<img width="300" height="300" alt="image" src="https://github.com/user-attachments/assets/583ca66b-f839-4c6f-85d7-7acbb4d194a9" />



Akhirnya, Poligon (misalnya, segi lima) merupakan kombinasi dari kedua konsep tersebut. Prosesnya dimulai dengan menentukan titik sudut (vertices) poligon menggunakan perhitungan trigonometri (sinus dan kosinus) berdasarkan radius tertentu. Setelah titik-titik sudut integer didapatkan, program kemudian mengiterasi melalui setiap sisi poligon, dan setiap sisi tersebut diubah menjadi serangkaian piksel diskrit menggunakan Algoritma Bresenham yang sama seperti yang digunakan untuk menggambar garis. Dengan demikian, poligon dihasilkan dengan merasterisasi (mengisi piksel) setiap segmen garis yang menghubungkan semua titik sudutnya.



<img width="300" height="300" alt="image" src="https://github.com/user-attachments/assets/06e89085-9f67-41f1-b718-30496981c8df" />
