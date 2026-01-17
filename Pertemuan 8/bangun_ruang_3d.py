
import pygame
from pygame.locals import *
from OpenGL.GL import *
import OpenGL.GLU as glu
import math

# ==========================================
# KONFIGURASI DAN VARIBEL GLOBAL
# ==========================================
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
DISPLAY_CAPTION = "Simulasi Bangun Ruang 3D - Edukatif & Interaktif"

# Warna (R, G, B)
COLOR_BG = (0.1, 0.1, 0.1, 1.0)
COLOR_TEXT = (255, 255, 255, 255)
COLOR_AXIS_X = (1.0, 0.0, 0.0) # Merah
COLOR_AXIS_Y = (0.0, 1.0, 0.0) # Hijau
COLOR_AXIS_Z = (0.0, 0.0, 1.0) # Biru

# Bangun Ruang Constants
SHAPE_CUBE = 0
SHAPE_CUBOID = 1
SHAPE_PYRAMID = 2
SHAPE_CYLINDER = 3
SHAPE_CONE = 4

SHAPE_NAMES = {
    SHAPE_CUBE: "KUBUS (Cube)",
    SHAPE_CUBOID: "BALOK (Cuboid)",
    SHAPE_PYRAMID: "LIMAS SEGIEMPAT (Pyramid)",
    SHAPE_CYLINDER: "TABUNG (Cylinder)",
    SHAPE_CONE: "KERUCUT (Cone)"
}

class GeometryApp:
    def __init__(self):
        pygame.init()
        self.display = (WINDOW_WIDTH, WINDOW_HEIGHT)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption(DISPLAY_CAPTION)

        # Inisialisasi OpenGL
        self.init_gl()

        # State Variable
        self.current_shape = SHAPE_CUBE
        self.auto_rotate = True
        self.rotation_angle = [0.0, 0.0, 0.0] # X, Y, Z
        self.translation = [0.0, 0.0, -5.0]  # X, Y, Z
        self.scale = 1.0
        self.reflection = False # Refleksi sumbu Y

        # Quadric untuk shape lengkung
        self.quadric = glu.gluNewQuadric()
        glu.gluQuadricDrawStyle(self.quadric, glu.GLU_FILL)

        # Auto-Cycle Variables
        self.auto_cycle = False
        self.last_cycle_time = 0
        self.cycle_interval = 3000 # 3 detik


    def init_gl(self):
        glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glu.gluPerspective(45, (WINDOW_WIDTH / WINDOW_HEIGHT), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST) # Mengaktifkan Depth Buffer agar gambar tidak tumpah tindih
        
        # Pencahayaan sederhana agar objek 3D terlihat lebih nyata
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glLightfv(GL_LIGHT0, GL_POSITION, (5, 5, 5, 1))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.8, 0.8, 0.8, 1))

    # ==========================
    # FUNGSI MENGGAMBAR BENTUK
    # ==========================
    def draw_axis(self):
        """Menggambar sumbu X, Y, Z untuk referensi"""
        glDisable(GL_LIGHTING)
        glBegin(GL_LINES)
        
        # Sumbu X - Merah
        glColor3fv(COLOR_AXIS_X)
        glVertex3f(-10.0, 0.0, 0.0)
        glVertex3f(10.0, 0.0, 0.0)

        # Sumbu Y - Hijau
        glColor3fv(COLOR_AXIS_Y)
        glVertex3f(0.0, -10.0, 0.0)
        glVertex3f(0.0, 10.0, 0.0)

        # Sumbu Z - Biru
        glColor3fv(COLOR_AXIS_Z)
        glVertex3f(0.0, 0.0, -10.0)
        glVertex3f(0.0, 0.0, 10.0)
        glEnd()
        glEnable(GL_LIGHTING)

    def draw_cube(self):
        # Titik sudut Kubus
        vertices = [
            (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
            (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
        ]
        surfaces = [
            (0,1,2,3), (3,2,6,7), (6,7,5,4),
            (4,5,1,0), (1,5,6,2), (4,0,3,7)
        ]
        colors = [
            (1,0,0), (0,1,0), (0,0,1), (1,1,0), (1,0,1), (0,1,1)
        ]

        glBegin(GL_QUADS)
        for i, surface in enumerate(surfaces):
            glColor3fv(colors[i % len(colors)]) # Warna berbeda tiap sisi
            glNormal3f(0, 0, 1) # Normal sederhana (tidak akurat utk semua sisi, tapi cukup utk flat shading simpel)
            for vertex in surface:
                glVertex3fv(vertices[vertex])
        glEnd()

    def draw_cuboid(self):
        # Balok adalah Kubus yang di-skala salah satu sisinya
        # Kita gambar manual saja biar jelas bedanya
        glPushMatrix()
        glScale(1.5, 0.8, 0.5) # Skala X lebih panjang, Y agak pendek
        self.draw_cube()
        glPopMatrix()

    def draw_pyramid(self):
        # Limas Segiempat
        vertices = [
            (1, -1, -1), (1, -1, 1), (-1, -1, 1), (-1, -1, -1), # Alas
            (0, 1, 0) # Puncak
        ]
        
        # Alas
        glBegin(GL_QUADS)
        glColor3f(1.0, 0.5, 0.0) # Oranye
        glVertex3fv(vertices[0]); glVertex3fv(vertices[1]); glVertex3fv(vertices[2]); glVertex3fv(vertices[3])
        glEnd()

        # Sisi Segitiga
        glBegin(GL_TRIANGLES)
        colors = [(1,0,0), (0,1,0), (0,0,1), (1,1,0)]
        faces = [(0,1,4), (1,2,4), (2,3,4), (3,0,4)]
        
        for i, face in enumerate(faces):
            glColor3fv(colors[i])
            for vertex_idx in face:
                glVertex3fv(vertices[vertex_idx])
        glEnd()

    def draw_cylinder(self):
        glColor3f(0.0, 0.8, 0.8) # Cyan
        glPushMatrix()
        glTranslatef(0, -1, 0) # Geser ke bawah sedikit biar di tengah
        glRotatef(-90, 1, 0, 0) # Putar agar berdiri tegak
        # gluCylinder(quad, baseRadius, topRadius, height, slices, stacks)
        glu.gluCylinder(self.quadric, 1.0, 1.0, 2.0, 32, 32)
        
        # Tutup Atas dan Bawah agar solid
        # Disk Bawah
        glu.gluDisk(self.quadric, 0, 1.0, 32, 32)
        # Disk Atas
        glPushMatrix()
        glTranslatef(0, 0, 2.0)
        glu.gluDisk(self.quadric, 0, 1.0, 32, 32)
        glPopMatrix()
        
        glPopMatrix()

    def draw_cone(self):
        glColor3f(1.0, 0.0, 1.0) # Magenta
        glPushMatrix()
        glTranslatef(0, -1, 0)
        glRotatef(-90, 1, 0, 0)
        # gluCylinder dengan topRadius=0 adalah Kerucut
        glu.gluCylinder(self.quadric, 1.0, 0.0, 2.5, 32, 32)
        
        # Tutup alas
        glu.gluDisk(self.quadric, 0, 1.0, 32, 32)
        glPopMatrix()

    # ==========================
    # TEXT RENDERING (OVERLAY)
    # ==========================
    def draw_text(self, x, y, text_string):
        """Menggambar teks 2D di atas scene 3D"""
        font = pygame.font.SysFont('Arial', 20)
        text_surface = font.render(text_string, True, (255, 255, 255, 255), (0,0,0,100))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glRasterPos2i(x, y)
        glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    # ==========================
    # LOGIKA UTAMA
    # ==========================
    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            # 1. Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    
                    # Ganti Bangun Ruang
                    elif event.key == pygame.K_1: self.current_shape = SHAPE_CUBE
                    elif event.key == pygame.K_2: self.current_shape = SHAPE_CUBOID
                    elif event.key == pygame.K_3: self.current_shape = SHAPE_PYRAMID
                    elif event.key == pygame.K_4: self.current_shape = SHAPE_CYLINDER
                    elif event.key == pygame.K_5: self.current_shape = SHAPE_CONE
                    
                    # Kontrol Transformasi
                    elif event.key == pygame.K_SPACE: 
                        self.auto_rotate = not self.auto_rotate # Toggle Rotasi
                    elif event.key == pygame.K_m: 
                        self.reflection = not self.reflection # Toggle Refleksi
                    elif event.key == pygame.K_r: # Reset
                        self.rotation_angle = [0.0, 0.0, 0.0]
                        self.translation = [0.0, 0.0, -5.0]
                        self.scale = 1.0
                        self.reflection = False
                    elif event.key == pygame.K_a:
                        self.auto_cycle = not self.auto_cycle # Toggle Auto-Cycle


            # Input Keyboard Continuous (Tahan tombol)
            keys = pygame.key.get_pressed()
            # Translasi (Panah)
            if keys[pygame.K_LEFT]: self.translation[0] -= 0.1
            if keys[pygame.K_RIGHT]: self.translation[0] += 0.1
            if keys[pygame.K_UP]: self.translation[1] += 0.1
            if keys[pygame.K_DOWN]: self.translation[1] -= 0.1
            # Zoom (W/S)
            if keys[pygame.K_w]: self.translation[2] += 0.1
            if keys[pygame.K_s]: self.translation[2] -= 0.1
            # Scale (Z/X)
            if keys[pygame.K_z]: self.scale += 0.05
            if keys[pygame.K_x]: self.scale = max(0.1, self.scale - 0.05)


            # 2. Update Logika
            if self.auto_rotate:
                self.rotation_angle[0] += 1.0
                self.rotation_angle[1] += 1.5

            # Auto-Cycle Functionality
            if self.auto_cycle:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_cycle_time > self.cycle_interval:
                    self.current_shape = (self.current_shape + 1) % 5
                    self.last_cycle_time = current_time


            # 3. Rendering Scene
            glClearColor(*COLOR_BG)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()

            # --- TRANSFORMASI GLOBAL (KAMERA / DUNIA) ---
            # Pindahkan seluruh dunia berdasarkan variable translation
            glTranslatef(self.translation[0], self.translation[1], self.translation[2])

            # Gambar Sumbu Referensi (Diam, tidak ikut berputar dgn objek)
            # Opsional: Jika ingin sumbu ikut translasi tapi tidak ikut rotasi objek
            self.draw_axis()

            # --- TRANSFORMASI OBJEK ---
            glPushMatrix() # Simpan matrix saat ini

            # 1. REFLEKSI (Pencerminan) - Opsional
            if self.reflection:
                # Cermin terhadap sumbu X (nilai Y dibalik) -> scale(1, -1, 1)
                # Atau Cermin terhadap sumbu Y (nilai X dibalik) -> scale(-1, 1, 1)
                glScalef(-1.0, 1.0, 1.0) 

            # 2. SKALA
            glScalef(self.scale, self.scale, self.scale)

            # 3. ROTASI
            glRotatef(self.rotation_angle[0], 1, 0, 0) # Putar sumbu X
            glRotatef(self.rotation_angle[1], 0, 1, 0) # Putar sumbu Y

            # --- GAMBAR OBJEK TERPILIH ---
            if self.current_shape == SHAPE_CUBE: self.draw_cube()
            elif self.current_shape == SHAPE_CUBOID: self.draw_cuboid()
            elif self.current_shape == SHAPE_PYRAMID: self.draw_pyramid()
            elif self.current_shape == SHAPE_CYLINDER: self.draw_cylinder()
            elif self.current_shape == SHAPE_CONE: self.draw_cone()

            glPopMatrix() # Kembalikan matrix

            # 4. Rendering UI (Overlay)
            # Tampilkan informasi di layar
            ui_y = WINDOW_HEIGHT - 30
            self.draw_text(10, ui_y, f"Bangun Ruang: {SHAPE_NAMES[self.current_shape]}")
            self.draw_text(10, ui_y - 25, f"Transformasi:")
            self.draw_text(20, ui_y - 50, f"- Rotasi (SPACE): {'ON' if self.auto_rotate else 'OFF'} [{int(self.rotation_angle[0])}, {int(self.rotation_angle[1])}]")
            self.draw_text(20, ui_y - 75, f"- Skala (Z/X): {self.scale:.2f}x")
            self.draw_text(20, ui_y - 100, f"- Posisi (Panah/WS): [{self.translation[0]:.1f}, {self.translation[1]:.1f}, {self.translation[2]:.1f}]")
            self.draw_text(20, ui_y - 125, f"- Refleksi/Cermin (M): {'ON' if self.reflection else 'OFF'}")
            
            self.draw_text(20, ui_y - 125, f"- Refleksi/Cermin (M): {'ON' if self.reflection else 'OFF'}")
            self.draw_text(20, ui_y - 150, f"- Auto-Ganti (A): {'ON' if self.auto_cycle else 'OFF'}")
            
            self.draw_text(10, 20, "KONTROL: 1-5 (Pilih) | A (Auto Ganti) | SPASI (Putar) | Z/X (Zoom) | M (Cermin) | R (Reset)")


            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    app = GeometryApp()
    app.run()
