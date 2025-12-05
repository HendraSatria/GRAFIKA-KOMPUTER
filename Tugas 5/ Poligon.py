import turtle
import sys
import math

# --- FUNGSI UTILITY: MENGGAMBAR TITIK DI TURTLE ---
def draw_points(points, scale=30, color="green"): # Warna diubah menjadi hijau untuk membedakan
    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.hideturtle()
    
    # Titik pusat (0,0) sebagai referensi
    t.goto(0, 0)
    t.dot(6, "red")

    for x, y in points:
        t.goto(x * scale, y * scale)
        t.dot(5, color)

# --- ALGORITMA GARIS BRESENHAM (Digunakan untuk menghubungkan titik-titik poligon) ---
def bresenham_line(x1, y1, x2, y2):
    """Mengimplementasikan Algoritma Bresenham (menangani semua kemiringan)."""
    
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    
    # Menentukan apakah garis curam (steep, |m| > 1)
    is_steep = dy > dx
    if is_steep:
        # Tukar x dan y untuk memastikan 0 <= m <= 1 (atau -1 <= m <= 0)
        x1, y1 = y1, x1
        x2, y2 = y2, x2
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        
    # Pastikan x1 <= x2 setelah penukaran
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        
    step_y = 1 if y2 > y1 else -1 
    
    x, y = x1, y1
    p = 2 * dy - dx
    
    while x <= x2:
        # Saat memplot, kembalikan posisi x dan y jika terjadi penukaran
        if is_steep:
            points.append((y, x))
        else:
            points.append((x, y))
        
        x += 1 
        
        if p >= 0:
            y += step_y
            p += 2 * (dy - dx)
        else:
            p += 2 * dy
            
    return points

# --- FUNGSI GENERATOR KOORDINAT SEGILIMA BERATURAN ---
def get_pentagon_vertices(r, center_x=0, center_y=0):
    """Menghasilkan 5 titik sudut (vertices) untuk segi lima beraturan."""
    vertices = []
    num_sides = 5
    # Sudut awal (90 derajat untuk membuat satu sisi tegak lurus)
    angle_offset = math.pi / 2 
    
    for i in range(num_sides):
        angle = angle_offset + i * 2 * math.pi / num_sides
        x = center_x + r * math.cos(angle)
        y = center_y + r * math.sin(angle)
        # Menggunakan round() untuk mendapatkan koordinat piksel integer
        vertices.append((round(x), round(y)))
        
    return vertices

# --- PROGRAM UTAMA POLIGON ---
if __name__ == "__main__":
    
    turtle.Screen().setup(width=600, height=600)
    turtle.resetscreen()

    print("--- Menggambar Segi Lima dengan Bresenham Line ---")
    
    R_PENTAGON = 8 # Radius (Jarak dari pusat ke sudut)
    
    # 1. Mendapatkan 5 titik sudut (vertices)
    vertices = get_pentagon_vertices(R_PENTAGON)
    
    all_polygon_points = []
    num_vertices = len(vertices)

    # 2. Menghitung titik piksel untuk setiap sisi menggunakan Bresenham
    for i in range(num_vertices):
        # Titik awal dan titik akhir (menggunakan modulo untuk menghubungkan titik terakhir ke titik pertama)
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % num_vertices] 
        
        line_points = bresenham_line(x1, y1, x2, y2)
        
        # Gabungkan semua titik
        all_polygon_points.extend(line_points)

    # 3. Gambar semua titik
    draw_points(all_polygon_points, scale=30, color="green")
    
    print(f"Segi Lima dengan radius {R_PENTAGON} selesai digambar ({len(all_polygon_points)} titik piksel).")
    
    try:
        turtle.done()
    except turtle.Terminator:
        pass