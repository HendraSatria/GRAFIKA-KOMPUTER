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

    for x, y in points:
        t.goto(x * scale, y * scale)
        t.dot(5, color)
    
# --- ALGORITMA GARIS BRESENHAM ---
def bresenham_line(x1, y1, x2, y2):
    """Mengimplementasikan Algoritma Bresenham (kasus 0 <= m <= 1)."""
    
    # Logika untuk memastikan x1 <= x2
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    
    step_y = 1 if y2 > y1 else -1 
    
    x, y = x1, y1
    p = 2 * dy - dx
    
    while x <= x2:
        points.append((x, y))
        
        x += 1 
        
        if p >= 0:
            y += step_y
            p += 2 * (dy - dx)
        else:
            p += 2 * dy
            
    return points

# --- PROGRAM UTAMA GARIS ---
if __name__ == "__main__":
    try:
        turtle.Screen().setup(width=600, height=600)
        turtle.resetscreen()
    except Exception:
        pass

    print("--- Menggambar Garis dengan Bresenham ---")
    
    # Contoh Garis: Dari (2, 3) ke (9, 7). Kemiringan positif, m < 1.
    x_start, y_start = 2, 3
    x_end, y_end = 9, 7
    line_points = bresenham_line(x_start, y_start, x_end, y_end)
    draw_points(line_points, scale=30, color="orange")
    
    print(f"Garis dari ({x_start}, {y_start}) ke ({x_end}, {y_end}) selesai digambar.")
    
    try:
        turtle.done()
    except turtle.Terminator:
        pass