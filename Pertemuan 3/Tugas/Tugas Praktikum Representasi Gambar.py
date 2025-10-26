import math

# === 1. GRID 10x10 DENGAN PIKSEL (4,6) ===
grid = [["." for _ in range(10)] for _ in range(10)]

# Koordinat piksel yang diganti
x, y = 4, 6
grid[y][x] = "X"

print("=== GRID 10x10 ===")
for row in grid:
    print(" ".join(row))

# === 2. GARIS DARI (0,0) KE (5,3) ===
x1, y1 = 0, 0
x2, y2 = 5, 3

dx = x2 - x1
dy = y2 - y1
steps = max(abs(dx), abs(dy))  # jumlah langkah tergantung jarak terpanjang
x_inc = dx / steps
y_inc = dy / steps

print("\n=== TITIK-TITIK GARIS (0,0) ke (5,3) ===")
x, y = x1, y1
for i in range(steps + 1):
    print(f"Langkah {i}: ({round(x)}, {round(y)})")
    x += x_inc
    y += y_inc

# === 3. TABEL PERBANDINGAN RASTER vs VEKTOR ===
print("\n=== TABEL PERBANDINGAN RASTER vs VEKTOR ===")
print(f"{'Aspek':30} {'Raster (Grid/Piksel)':40} {'Vektor (Titik & Garis Matematis)'}")
print("-"*110)
print(f"{'Representasi data':30} {'Disusun dari piksel di grid':40} {'Didefinisikan oleh rumus, titik, dan garis'}")
print(f"{'Ketika diperbesar':30} {'Gambar menjadi pecah (blur)':40} {'Gambar tetap tajam (berbasis rumus)'}")
print(f"{'Contoh implementasi':30} {'Bitmap, foto, peta piksel':40} {'SVG, CAD, logo desain'}")
print(f"{'Ukuran file':30} {'Lebih besar (tergantung resolusi)':40} {'Lebih kecil dan efisien'}")
print(f"{'Pengolahan':30} {'Mudah diubah per piksel':40} {'Butuh perhitungan matematis'}")
print(f"{'Contoh praktikum':30} {'Grid 10x10 dengan 1 piksel X':40} {'Garis (0,0) ke (5,3) dengan koordinat'}")

 