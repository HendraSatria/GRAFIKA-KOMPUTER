import turtle
import math
import random


# SETUP LAYAR

screen = turtle.Screen()

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()
pen.pensize(2)

# Inisialisasi assets
screen.addshape("cloud_small.gif")
screen.addshape("cloud_medium.gif")
screen.addshape("cloud_large.gif")

screen.title("Mini Scene 2D - Grafika Komputer")
screen.setup(900, 600)
screen.bgcolor("#87CEEB")  # Biru Narural
screen.tracer(0)

# Bulan
screen.addshape("bulan.gif") 
moon_sprite = turtle.Turtle()
moon_sprite.penup()
moon_sprite.hideturtle()
moon_sprite.speed(0)

# Awan
cloud = turtle.Turtle()
cloud.penup()
cloud.hideturtle()
cloud.speed(0)
cloud_x = random.randint(-500, -300)
cloud_y = random.randint(180, 260)
cloud_scale = random.randint(0, 2)
scale_dir = random.choice([1, -1])
cloud_speed = random.randint(1, 3)
cloud_active = True


# ALGORITMA DDA 

def draw_line_dda(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    steps = int(max(abs(dx), abs(dy)))
    x_inc = dx / steps
    y_inc = dy / steps

    x, y = x1, y1
    pen.penup()
    pen.goto(round(x), round(y))
    pen.pendown()

    for _ in range(steps):
        x += x_inc
        y += y_inc
        pen.goto(round(x), round(y))


# MIDPOINT CIRCLE UNTUK MATAHARI 

def draw_circle_midpoint(xc, yc, r):
    x = 0
    y = r
    p = 1 - r

    def plot(x, y):
        points = [
            (xc + x, yc + y), (xc - x, yc + y),
            (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x),
            (xc + y, yc - x), (xc - y, yc - x)
        ]
        for px, py in points:
            pen.penup()
            pen.goto(px, py)
            pen.pendown()
            pen.dot(4)

    plot(x, y)
    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1
        plot(x, y)

# ROTASI TITIK MATAHARI

def rotate_point(x, y, xc, yc, angle):
    rad = math.radians(angle)
    x -= xc
    y -= yc

    xr = x * math.cos(rad) - y * math.sin(rad)
    yr = x * math.sin(rad) + y * math.cos(rad)

    return xr + xc, yr + yc

# TRANSLASI TITIK 2D

def translate_point(x, y, tx, ty):
    return x + tx, y + ty


# POLIGON UNTUK MEMBUAT RUMAH 

def draw_polygon(points, fill_color=None):
    pen.penup()
    pen.goto(points[0])
    pen.pendown()

    if fill_color:
        pen.fillcolor(fill_color)
        pen.begin_fill()

    for p in points[1:]:
        pen.goto(p)
    pen.goto(points[0])

    if fill_color:
        pen.end_fill()
        
        
# GAMBAR DANAU & REFLEKSI

def draw_water():
    
    pen.color("#4682B4") # Warna BIRU 
    draw_polygon(
        [(-500, -200), (500, -200), (500, -400), (-500, -400)],
        "#4682B4"
    )

def draw_mountains():
    # Gunung Jauh 
    pen.color("#4682B4") 
    draw_polygon([(-500, -200), (-250, 50), (0, -200)], "#4682B4")
    draw_polygon([(0, -200), (250, 100), (500, -200)], "#4682B4")
    
    # Gunung Dekat 
    pen.color("#2F4F4F") 
    draw_polygon([(-400, -200), (-150, 0), (100, -200)], "#2F4F4F")
    draw_polygon([(50, -200), (300, 20), (550, -200)], "#2F4F4F")

   

def draw_house_reflection():
    # Garis cermin DARI AIR
    mirror_y = -200
    
    # Refleksi Badan Rumah
   
    body_points = [(-120, -200), (120, -200), (120, 0), (-120, 0)]
    refl_body = reflect_y(body_points, mirror_y)
    draw_polygon(refl_body, "#36648B") 

    # Refleksi Atap
    
    roof_points = [(-140, 0), (0, 120), (140, 0)]
    refl_roof = reflect_y(roof_points, mirror_y)
    draw_polygon(refl_roof, "#5D0000") 
    
    # Air 
    pen.color("#B0C4DE")
    for i in range(1, 4):
        y_ripple = mirror_y - (i * 40)
        draw_line_dda(-200, y_ripple, 200, y_ripple)



# GAMBAR RUMAH

def draw_house():
    # Badan rumah
    pen.color("black")
    draw_polygon(
        [(-120, -200), (120, -200), (120, 0), (-120, 0)],
        "#F5DEB3"
    )

    # Atap
    draw_polygon(
        [(-140, 0), (0, 120), (140, 0)],
        "#8B0000"
    )

    # Pintu
    draw_polygon(
        [(-25, -200), (25, -200), (25, -80), (-25, -80)],
        "#654321"
    )

    # Jendela kiri
    draw_polygon(
        [(-90, -60), (-40, -60), (-40, -20), (-90, -20)],
        "#ADD8E6"
    )

    # Jendela kanan
    draw_polygon(
        [(40, -60), (90, -60), (90, -20), (40, -20)],
        "#ADD8E6"
    )

# AWAN DENGAN TRANSFORMASI SKALA 

def draw_scaling_cloud(x, y, scale_step):
    if scale_step == 0:
        cloud.shape("cloud_small.gif")
    elif scale_step == 1:
        cloud.shape("cloud_medium.gif")
    else:
        cloud.shape("cloud_large.gif")

    cloud.goto(x, y)
    cloud.showturtle()

# RESET AWAN RANDOM

def reset_cloud():
    global cloud_x, cloud_y, cloud_scale, scale_dir, cloud_speed, cloud_active

    cloud_x = random.randint(-500, -300)
    cloud_y = random.randint(180, 260)

    cloud_scale = random.randint(0, 2)
    scale_dir = random.choice([1, -1])

    cloud_speed = random.randint(1, 3)
    cloud_active = True

    cloud.hideturtle()


# GAMBAR JALAN

def draw_road():
    draw_polygon(
        [(-500, -200), (500, -200), (500, -250), (-500, -250)],
        "#555555"
    )

    pen.color("white")
    for x in range(-450, 500, 60):
        draw_line_dda(x, -225, x + 30, -225)


# MATAHARI ROTASI + TRANSLASI

def draw_rotating_translating_sun(angle, tx):
    base_x, base_y = 200, 180
    r = 35

    # Translasi pusat matahari
    xc = base_x + tx
    yc = base_y

    pen.color("yellow")
    draw_circle_midpoint(xc, yc, r)

    # Sinar matahari (rotasi)
    for i in range(0, 360, 30):
        base_angle = i + angle

        x1 = xc + r * math.cos(math.radians(base_angle))
        y1 = yc + r * math.sin(math.radians(base_angle))
        x2 = xc + (r + 20) * math.cos(math.radians(base_angle))
        y2 = yc + (r + 20) * math.sin(math.radians(base_angle))

        draw_line_dda(x1, y1, x2, y2)


# SKALA & REFLEKSI TITIK 

def scale_point(x, y, xc, yc, s):
    x -= xc
    y -= yc
    return xc + x * s, yc + y * s

def reflect_y(points, yc):
   
    return [(x, 2 * yc - y) for x, y in points]
def draw_sun_reflection(angle, tx):
    base_x, base_y = 200, 180
    r = 35
    mirror_y = -200 # Garis air
    
    # Pusat matahari asli
    xc = base_x + tx
    yc = base_y
    
 
    refl_pos = reflect_y([(xc, yc)], mirror_y)[0]
    rxc, ryc = refl_pos
    
    for i in range(5):
        pen.color("#FFD700") 
        
        offset_y = ryc - (i * 10)
        width = (r + 10) - (i * 5)
        if width > 0:
            draw_line_dda(rxc - width, offset_y, rxc + width, offset_y)
            

    for i in range(0, 360, 60): 
        base_angle = -(i + angle) 
        
     
        x1, y1 = rxc + (r/2) * math.cos(math.radians(base_angle)), ryc + (r/2) * math.sin(math.radians(base_angle))
        x2, y2 = rxc + (r) * math.cos(math.radians(base_angle)), ryc + (r) * math.sin(math.radians(base_angle))
        
        pen.color("#FFA500") # Orange pudar
        draw_line_dda(x1, y1, x2, y2)
        
def draw_moon(tx):
    # Koordinat dasar 
    base_x, base_y = 200, 180
    xc = base_x + tx
    yc = base_y

    moon_sprite.goto(xc, yc)
    moon_sprite.shape("bulan.gif")
    
    # mode malam
    if sky_mode == MODE_MOON:
        moon_sprite.showturtle()
    else:
        moon_sprite.hideturtle()

        


def update_sky_sync(mode):
    """Ganti fungsi update_sky lama dengan ini"""
    if mode == MODE_SUN:
        screen.bgcolor("#87CEEB")  # Biru Cerah (Siang)
    elif mode == MODE_MOON:
        screen.bgcolor("#0B1D3A")  # Biru Gelap (Malam)

  
def draw_grass():
    pen.color("#006400")  # Hijau tua
    for x in range(-500, 500, 8):
        height = random.randint(8, 16)
        draw_line_dda(x, -200, x, -200 + height)

def draw_tree(x, y, size):
    # Batang pohon
    pen.pensize(size / 10)
    pen.color("#4B2C20") # Cokelat gelap
    draw_line_dda(x, y, x, y + size)
    
    # Daun 
    pen.color("#1A522E") # Hijau tua
    for _ in range(15):
        rx = x + random.randint(-int(size/2), int(size/2))
        ry = y + size + random.randint(-int(size/3), int(size/3))
        pen.penup()
        pen.goto(rx, ry)
        pen.dot(random.randint(15, 30))
        
        
#     UNTUK BINTANG 
stars = [(random.randint(-450, 450), random.randint(50, 280)) for _ in range(50)]

def draw_stars():
    for x, y in stars:
        size = random.choice([2, 3]) # Efek kelap-kelip kecil
        pen.penup()
        pen.goto(x, y)
        pen.color("white")
        pen.dot(size)


def draw_bird(x, y, fase):
    #  gerakan sayap 
    # fase akan berganti 
    wing_offset = [10, 0, -10][fase] 
    
    pen.pensize(2)
    pen.color("#1A1A1A") 
    
    # Sayap Kiri
    draw_line_dda(x, y, x - 15, y + wing_offset)
    # Sayap Kanan
    draw_line_dda(x, y, x + 15, y + wing_offset)
    
    pen.pensize(2) 
  
birds = [
    {"x": -500, "y": 200, "speed": 3, "wing_fase": 0},
    {"x": -550, "y": 230, "speed": 2.5, "wing_fase": 1}
]

                                            # MAIN PROGRAM


angle = 0
tx = -500
speed = 2
reset_pos = 500
def draw_lamp(x, y, is_on=False):
  # Tiang Lampu 
    pen.pensize(3) 
    pen.color("#2C3E50") 
    draw_line_dda(x, y, x, y + 120) 
    
    #Ornamen Lengan Lampu 
    draw_line_dda(x, y + 120, x + 15, y + 115)
    
    # Kap LAMPU
    kap_points = [
        (x + 10, y + 115), (x + 20, y + 115), 
        (x + 22, y + 120), (x + 8, y + 120)
    ]
    draw_polygon(kap_points, "#1A1A1A")
    
    # Kap Lampu 2
    kap_points = [
        (x + 10, y + 115), (x + 20, y + 115), 
        (x + 22, y + 120), (x + 8, y + 120)
    ]
    draw_polygon(kap_points, "#1A1A1A")
    
    # Cahaya 
    if is_on:
        # a. Sinar Inti 
        beam_core = [
            (x + 12, y + 115), (x + 18, y + 115), 
            (x + 50, y - 50), (x - 20, y - 50)
        ]
        draw_polygon(beam_core, "#FFFDE7") 
        
        # b. Sinar LuaR
        beam_glow = [
            (x + 10, y + 115), (x + 20, y + 115), 
            (x+40, y-20), (x-40, y-20)
        ]
        draw_polygon(beam_glow, "#FFFDE7") # Sangat pudar
        
        # c. Titik Lampu 
        pen.penup()
        pen.goto(x + 15, y + 116)
        pen.color("")
        pen.dot(12)
    
    pen.pensize(2) 

# SIANG & MALAM

day_time = True      
cycle_counter = 0   # Penghitung waktu
DAY_DURATION = 180  # DURASI SIANG


# STATE LANGIT

MODE_SUN = "sun"
MODE_MOON = "moon"
MODE_EMPTY = "empty"

sky_mode = MODE_SUN
empty_counter = 0
EMPTY_DELAY = 10  # jumlah frame langit kosong

while True:
 
    update_sky_sync(sky_mode)
    pen.clear()
    draw_mountains()
    draw_water()
    draw_house_reflection()
    lampu_nyala = (sky_mode == MODE_MOON)
    

    # ANIMASI BURUNG (Hanya saat Siang)
    if sky_mode == MODE_SUN:
        for bird in birds:
            draw_bird(bird["x"], bird["y"], bird["wing_fase"])
            
            # Gerakkan posisi burung
            bird["x"] += bird["speed"]
            
            # Update fase sayap (setiap beberapa frame)
            if int(bird["x"]) % 10 == 0:
                bird["wing_fase"] = (bird["wing_fase"] + 1) % 3
            
            # Reset jika keluar layar
            if bird["x"] > 500:
                bird["x"] = -550
                bird["y"] = random.randint(150, 250)

   
    
    # Gambar lampu di beberapa titik (misalnya di samping rumah atau jalan)
    draw_lamp(-180, -200, is_on=lampu_nyala) # Lampu kiri
    draw_lamp(180, -200, is_on=lampu_nyala)  # Lampu kanan

    # BENDA LANGIT
    if sky_mode == MODE_SUN:
        draw_rotating_translating_sun(angle, tx)
        draw_sun_reflection(angle, tx) 
        angle += 5
        tx += speed
        if tx > reset_pos:
            sky_mode = MODE_EMPTY
            next_mode = MODE_MOON # Habis matahari, gilirannya bulan
            empty_counter = 0

    elif sky_mode == MODE_MOON:
        draw_moon(tx)
        draw_stars()
       
        tx += speed
        if tx > reset_pos:
            sky_mode = MODE_EMPTY
            next_mode = MODE_SUN # Habis bulan, gilirannya matahari
            empty_counter = 0

    elif sky_mode == MODE_EMPTY:
        empty_counter += 1
        if empty_counter > EMPTY_DELAY:
            tx = -reset_pos
            angle = 0
            sky_mode = next_mode # Aktifkan mode selanjutnya
            
            
            
#    MEMUNCULKAN AWAN (SIANG)
    if sky_mode == MODE_SUN:
        if cloud_active:
            draw_scaling_cloud(cloud_x, cloud_y, cloud_scale)
            cloud_x += cloud_speed
            
            # Animasi Skala
            cloud_scale += scale_dir
            if cloud_scale > 2 or cloud_scale < 0:
                scale_dir *= -1
                cloud_scale += scale_dir

            if cloud_x > 500:
                cloud_active = False
                cloud.hideturtle()
        else:
            reset_cloud()
    else:
        # sembunyikan awan
        cloud.hideturtle()
        # reset posisi awan agar 
        cloud_x = -500
    
    # GAMBAR OBJEK DEPAN 
    draw_tree(-380, -200, 90) # Pohon kiri
    draw_tree(380, -200, 80)  # Pohon kanan
    draw_grass()
    draw_road()
    draw_house()

    # UPDATE SCREEN
    screen.update()
 
