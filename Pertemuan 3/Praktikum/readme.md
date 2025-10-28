# File: Reppresentasi Raster.py
## 1 — Membuat Grid Dasar 10x5 
```python

for y in range(0, 5):
    for x in range(0, 10):
        print(".", end="")
    print()
```
Kode ini mencetak grid 10 kolom × 5 baris menggunakan karakter ".", yang mewakili piksel kosong.
Ini adalah dasar dari representasi raster, di mana setiap titik di layar diwakili oleh posisi (x, y) pada grid.

## — Menghitung Jarak dan Kuadran
```python
x1 = float(input("\nMasukkan koordinat x1: "))
y1 = float(input("Masukkan koordinat y1: "))
x2 = float(input("Masukkan koordinat x2: "))
y2 = float(input("Masukkan koordinat y2: "))

jarak = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
```
Program menerima input dua titik koordinat, lalu menghitung jaraknya menggunakan rumus Euclidean distance:
<img width="226" height="46" alt="image" src="https://github.com/user-attachments/assets/d596e8fa-559c-4f41-8a86-54466e65a4cf" />


Kemudian dilakukan identifikasi posisi titik pertama ke dalam salah satu kuadran kartesius (I, II, III, IV) atau sumbu X/Y.

## — Menampilkan Titik “X” pada Grid
```python
lebar = 10
tinggi = 5
x_titik = 3
y_titik = 2
```
Bagian ini menampilkan titik tertentu (“X”) di dalam grid 10x5:Titik (x_titik, y_titik) diberi tanda "X".
Titik lain ditampilkan dengan ".".Output-nya menggambarkan bagaimana piksel tunggal direpresentasikan pada layar, sesuai konsep grafika raster.
<img width="430" height="431" alt="image" src="https://github.com/user-attachments/assets/aa2f0746-bf5b-4a49-9f6e-7f7dd93c934c" />

# File: Representasi Vektor.py
```phython
x1, y1 = 0, 0
x2, y2 = 5, 3

n = 5
for i in range(n + 1):
    x = x1 + (x2 - y1)*1 /n
    y = x1 + (x2 - y1)*1 /n
    print(f"Titik ke-{i}: ({x:.1f},{y:.1f})")
```
menjelaskan konsep grafika vektor, yaitu bagaimana garis atau bentuk geometris dibentuk menggunakan rumus matematika antara
dua titik koordinat. Dalam kode, didefinisikan titik awal (0,0) dan titik akhir (5,3), lalu program menghitung beberapa titik
di antara keduanya dengan membagi garis menjadi beberapa segmen. Meskipun terdapat sedikit kesalahan pada rumus interpolasinya,
ide utama program ini adalah menunjukkan bahwa setiap titik pada garis dapat dihitung secara proporsional menggunakan persamaan linear.
Konsep ini menggambarkan bahwa dalam grafika vektor, gambar tidak bergantung pada jumlah piksel, tetapi pada perhitungan koordinat,
sehingga tetap tajam dan presisi meskipun diperbesar.
<img width="308" height="116" alt="image" src="https://github.com/user-attachments/assets/ec2094b4-5bed-42c5-a11e-08d4a2f43ee9" />
