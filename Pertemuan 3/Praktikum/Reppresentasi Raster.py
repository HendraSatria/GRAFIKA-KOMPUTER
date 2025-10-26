import math

# Membuat grid dasar 10x5
for y in range(0, 5):
    for x in range(0, 10):
        print(".", end="")
    print()

# === Soal 1: Hitung jarak dan tentukan kuadran ===
x1 = float(input("\nMasukkan koordinat x1: "))
y1 = float(input("Masukkan koordinat y1: "))
x2 = float(input("Masukkan koordinat x2: "))
y2 = float(input("Masukkan koordinat y2: "))

# Rumus jarak dua titik
jarak = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Menentukan kuadran titik pertama
if x1 > 0 and y1 > 0:
    kuadran = "Kuadran I"
elif x1 < 0 and y1 > 0:
    kuadran = "Kuadran II"
elif x1 < 0 and y1 < 0:
    kuadran = "Kuadran III"
elif x1 > 0 and y1 < 0:
    kuadran = "Kuadran IV"
elif x1 == 0 and y1 == 0:
    kuadran = "Titik Pusat (0,0)"
elif x1 == 0:
    kuadran = "Berada di Sumbu Y"
elif y1 == 0:
    kuadran = "Berada di Sumbu X"

print(f"\nTitik pertama: ({x1}, {y1})")
print(f"Titik kedua  : ({x2}, {y2})")
print(f"Jarak antara dua titik = {jarak:.2f}")
print(f"Titik pertama berada di: {kuadran}")

# === Soal 2: Menampilkan titik X pada grid ===
lebar = 10
tinggi = 5
x_titik = 3
y_titik = 2

print("\n=== Simulasi Koordinat 10x5 ===\n")
for y in range(tinggi - 1, -1, -1):
    for x in range(lebar):
        if x == x_titik and y == y_titik:
            print("X", end="")  # tampilkan titik
        else:
            print(".", end="")  # latar kosong
    print()
