import turtle
import sys

# --- FUNGSI UTILITY: MENGGAMBAR TITIK DI TURTLE ---
def draw_points(points, scale=20, color="black"):
    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.hideturtle()
    
    # Titik pusat (0,0)
    t.goto(0, 0)
    t.dot(6, "red")

    for x, y in points:
        t.goto(x * scale, y * scale)
        t.dot(5, color)
    
# --- ALGORITMA MIDPOINT CIRCLE ---
def plot_circle_points(x, y, xc, yc, all_points):
    """Menambahkan 8 titik simetris (octants) ke list points."""
    # Asumsi pusat (xc, yc) = (0, 0)
    all_points.append((xc + x, yc + y))
    all_points.append((xc + y, yc + x))
    all_points.append((xc - y, yc + x))
    all_points.append((xc - x, yc + y))
    all_points.append((xc - x, yc - y))
    all_points.append((xc - y, yc - x))
    all_points.append((xc + y, yc - x))
    all_points.append((xc + x, yc - y))
    return all_points

def midpoint_circle(r, xc=0, yc=0):
    """Mengimplementasikan Algoritma Midpoint Circle."""
    all_points = []
    x = 0
    y = r # Mulai dari (0, r)
    p = 1 - r # Variabel keputusan awal
    
    plot_circle_points(x, y, xc, yc, all_points)

    while x < y: # Ulangi selama x < y
        x += 1 # Tambah x sebanyak 1
        if p < 0: # Jika p < 0
            p = p + 2 * x + 3 
        else: # Jika p >= 0
            y -= 1 # y = y - 1
            p = p + 2 * (x - y) + 5 
        
        plot_circle_points(x, y, xc, yc, all_points)
    
    return all_points

# --- PROGRAM UTAMA LINGKARAN ---
if __name__ == "__main__":
    try:
        turtle.Screen().setup(width=600, height=600)
        turtle.resetscreen()
    except Exception:
        pass

    print("--- Menggambar Lingkaran dengan Midpoint Circle ---")
    
    r_circle = 6 # Radius 6 (seperti contoh di slide)
    circle_points = midpoint_circle(r_circle)
    draw_points(circle_points, scale=30, color="blue")
    
    print(f"Lingkaran dengan radius {r_circle} selesai digambar.")
    
    try:
        turtle.done()
    except turtle.Terminator:
        pass