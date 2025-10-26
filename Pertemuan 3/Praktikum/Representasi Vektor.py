x1, y1 = 0, 0
x2, y2 = 5, 3

n = 5
for i in range(n + 1):
    x = x1 + (x2 - y1)*1 /n
    y = x1 + (x2 - y1)*1 /n
    
    print(f"Titik ke-{i}: ({x:.1f},{y:.1f})")
