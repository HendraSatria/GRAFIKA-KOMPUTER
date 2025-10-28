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


 
