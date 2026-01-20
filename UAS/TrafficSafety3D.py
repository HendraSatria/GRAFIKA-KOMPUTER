
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
        
# --- KONFIGURASI ---
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
GAME_TITLE = "Traffic Simulator 3D: Complete Education Edition"
FPS = 60

# --- UTILS ---
def draw_text_on_screen(text_surface, x, y, window_width, window_height):
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    w, h = text_surface.get_size()
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glRasterPos2i(x, window_height - y - h)
    glDrawPixels(w, h, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

# --- TEXTURE MANAGER ---
class TextureManager:
    textures = {}
    @staticmethod
    def generate_surface(width, height, type="noise"):
        surface = pygame.Surface((width, height))
        if type == "asphalt":
            surface.fill((30, 30, 30))
            for _ in range(800): 
                surface.set_at((random.randint(0, width-1), random.randint(0, height-1)), (random.randint(20, 60),)*3)
        elif type == "grass":
            surface.fill((34, 100, 34)) 
            for _ in range(4000): 
                surface.set_at((random.randint(0, width-1), random.randint(0, height-1)), (30, random.randint(60, 140), 30))
        elif type == "mountain":
            surface.fill((80, 80, 90)); 
            for _ in range(400): 
                surface.set_at((random.randint(0, width-1), random.randint(0, int(height/2.5))), (240, 240, 255))
        elif type == "bark":
            surface.fill((60, 40, 20))
            for _ in range(100): 
                pygame.draw.rect(surface, (40, 20, 10), (random.randint(0, width-1), 0, random.randint(2, 5), height))
        elif type == "leaf":
            surface.fill((10, 60, 10))
            for _ in range(2000): 
                surface.set_at((random.randint(0, width-1), random.randint(0, height-1)), (20, random.randint(40, 100) + 20, 20))
        return surface

    @staticmethod
    def load_texture(name, surface):
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, surface.get_width(), surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(surface, "RGBA", 1))
        TextureManager.textures[name] = tex_id
        return tex_id
        
    @staticmethod
    def get(name): return TextureManager.textures.get(name)

# --- SYSTEMS ---
class DayNightSystem:
    def __init__(self):
        self.state = "SIANG"
        self.timer = 0
        self.duration = 60000
        self.colors = {"SIANG": ((0.4, 0.7, 0.95, 1), (0.9, 0.9, 0.8, 1)), "SORE": ((0.8, 0.5, 0.2, 1), (0.8, 0.6, 0.3, 1)), "MALAM": ((0.05, 0.05, 0.1, 1), (0.2, 0.2, 0.35, 1))}
        self.sun_pos = [0, 100, 0, 0]
        self.current = self.colors["SIANG"]
        
    def update(self, dt):
        self.timer += dt
        cycle = self.timer % (self.duration * 3)
        if cycle < self.duration: 
            self.state, self.current, self.sun_pos = "SIANG", self.colors["SIANG"], [-50, 100, 50, 0]
        elif cycle < self.duration * 2: 
            self.state, self.current, self.sun_pos = "SORE", self.colors["SORE"], [-80, 20, 50, 0]
        else: 
            self.state, self.current, self.sun_pos = "MALAM", self.colors["MALAM"], [20, 80, -20, 0]
            
    def apply(self):
        glClearColor(*self.current[0])
        glLightfv(GL_LIGHT0, GL_POSITION, self.sun_pos)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.current[1])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [c * 0.4 for c in self.current[1]])

class AudioSystem:
    def __init__(self):
        try: 
            pygame.mixer.init()
            self.enabled = True
        except Exception as e: 
            print(f"Audio system disabled: {e}")
            self.enabled = False
        self.sounds = {}
        for n in ["horn", "crash", "skid", "engine"]: 
            self.load(n, f"assets/{n}.wav")
            
    def load(self, n, f): 
        try: 
            self.sounds[n] = pygame.mixer.Sound(f) if self.enabled else None
            if self.sounds[n] is None and self.enabled:
                print(f"Warning: Could not load sound {n} from {f}")
        except Exception as e: 
            print(f"Error loading sound {n}: {e}")
            
    def play(self, n): 
        if self.enabled and self.sounds.get(n): 
            self.sounds[n].play()

# --- DRAWING ---
def draw_box(size, color=None, texture_name=None, repeat_x=1, repeat_y=1):
    x, y, z = size
    tex_id = TextureManager.get(texture_name) if texture_name else None
    
    if tex_id: 
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glColor3f(1,1,1)
    elif color: 
        glDisable(GL_TEXTURE_2D)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color + (1.0,))
        glColor3fv(color)
        
    verts = [( x, -y, -z), ( x,  y, -z), (-x,  y, -z), (-x, -y, -z), ( x, -y,  z), ( x,  y,  z), (-x,  y,  z), (-x, -y,  z)]
    uvs = [(0,0), (repeat_x,0), (repeat_x,repeat_y), (0,repeat_y)]
    faces = [(0,1,2,3), (4,5,6,7), (2,6,7,3), (0,4,5,1), (1,5,6,2), (0,3,7,4)]
    norms = [(0,0,-1), (0,0,1), (-1,0,0), (1,0,0), (0,1,0), (0,-1,0)]
    
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        glNormal3fv(norms[i])
        for j, v_idx in enumerate(face):
            if tex_id: glTexCoord2f(uvs[j][0], uvs[j][1])
            glVertex3fv(verts[v_idx])
    glEnd()
    if tex_id: glDisable(GL_TEXTURE_2D)

def draw_pyramid_tex(size, tex, color):
    x, y, z = size
    tex_id = TextureManager.get(tex)
    if tex_id: 
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glColor3f(1,1,1)
    else: 
        glDisable(GL_TEXTURE_2D)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, color + (1.0,))
        glColor3fv(color)
        
    glBegin(GL_TRIANGLES)
    norms = [(0,0.5,1), (1,0.5,0), (0,0.5,-1), (-1,0.5,0)]
    faces = [((0,y,0),(-x,-y,z),(x,-y,z)), ((0,y,0),(x,-y,z),(x,-y,-z)), ((0,y,0),(x,-y,-z),(-x,-y,-z)), ((0,y,0),(-x,-y,-z),(-x,-y,z))]
    t_coords = [(0.5,1), (0,0), (1,0)]
    
    for i, face in enumerate(faces):
        glNormal3f(*norms[i])
        for j, v in enumerate(face): 
            if tex_id: glTexCoord2f(*t_coords[j])
            glVertex3f(*v)
    glEnd()
    glDisable(GL_TEXTURE_2D)

def draw_tree_realistic():
    glPushMatrix()
    glScalef(0.6, 2.0, 0.6)
    draw_box((1,1,1), texture_name="bark")
    glPopMatrix()
    for y_off, scale in [(2.5, 3.0), (4.0, 2.2), (5.5, 1.2)]:
        glPushMatrix()
        glTranslatef(0, y_off, 0)
        draw_pyramid_tex((scale, scale*0.8 + 0.5, scale), "leaf", (0.1, 0.4, 0.1))
        glPopMatrix()

# --- GAME OBJECTS ---

class TrafficLight:
    def __init__(self, z_pos):
        self.z = z_pos; self.x = -12; self.state = "GREEN"; self.timer = 0
    def update(self):
        self.timer += 1
        if self.state == "GREEN" and self.timer > 300: self.state = "YELLOW"; self.timer = 0
        elif self.state == "YELLOW" and self.timer > 120: self.state = "RED"; self.timer = 0
        elif self.state == "RED" and self.timer > 300: self.state = "GREEN"; self.timer = 0
    def draw(self, is_night):
        glPushMatrix()
        glTranslatef(self.x, 0, self.z)
        glDisable(GL_TEXTURE_2D)
        glData = gluNewQuadric()
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        gluCylinder(glData, 0.3, 0.3, 6.0, 16, 1) # Tiang
        glPopMatrix()
        
        glTranslatef(0, 6.0, 0)
        glRotatef(90, 0, 1, 0)
        glPushMatrix()
        glTranslatef(0, 0, 1.5)
        glScalef(0.2, 0.2, 3.0)
        draw_box((1,1,1), color=(0.5,0.5,0.5)) # Lengan
        glPopMatrix()
        
        glTranslatef(0, -0.5, 4.0)
        glPushMatrix()
        glScalef(0.8, 2.0, 0.8)
        draw_box((1,1,1), color=(0.2,0.2,0.2)) # Box
        glPopMatrix()
        
        for off, col, st in [(1.2,(1,0,0),"RED"), (0,(1,1,0),"YELLOW"), (-1.2,(0,1,0),"GREEN")]:
            active = self.state == st
            glPushMatrix()
            glTranslatef(0, off, 0.85)
            glScalef(0.5,0.5,0.1)
            glMaterialfv(GL_FRONT, GL_EMISSION, col + (1.0,) if active else (0,0,0,1))
            draw_box((1,1,1), color=col if active else tuple(c*0.2 for c in col))
            glPopMatrix()
        glMaterialfv(GL_FRONT, GL_EMISSION, (0,0,0,1))
        glPopMatrix()

class ZebraCross:
    def __init__(self, z_pos):
        self.z = z_pos; self.width = 10; self.depth = 4
    def draw(self, is_night):
        glPushMatrix()
        glTranslatef(0, 0.03, self.z)
        glMaterialfv(GL_FRONT, GL_EMISSION, (0.3, 0.3, 0.3, 1) if is_night else (0,0,0,1))
        for i in range(-9, 11, 2):
            glPushMatrix()
            glTranslatef(i, 0, 0)
            glScalef(0.7, 0.01, self.depth/2)
            draw_box((1,1,1), color=(1,1,1))
            glPopMatrix()
        glMaterialfv(GL_FRONT, GL_EMISSION, (0,0,0,1))
        glPopMatrix()

class Pedestrian:
    def __init__(self, z_pos):
        self.z = z_pos; self.x = -15; self.direction = 1; self.speed = 0.05
        self.wobble = 0; self.color = (random.random(), random.random(), random.random())
    def update(self):
        self.x += self.speed * self.direction; self.wobble += 0.2
        if self.x > 15: self.direction = -1
        if self.x < -15: self.direction = 1
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, 1.2, self.z)
        glRotatef(90 if self.direction > 0 else -90, 0, 1, 0)
        # Balok Badan 
        glPushMatrix()
        glScalef(0.4, 0.7, 0.25)
        draw_box((1,1,1), color=self.color)
        glPopMatrix()
        # Kepala
        glPushMatrix()
        glTranslatef(0, 0.9, 0)
        glScalef(0.22, 0.22, 0.22)
        draw_box((1,1,1), color=(0.9, 0.8, 0.7))
        glPopMatrix()
        # Kaki Translasi Anim
        leg_rot = math.sin(self.wobble) * 20
        glPushMatrix()
        glTranslatef(0, -0.6, 0.15)
        glRotatef(leg_rot, 1, 0, 0)
        glTranslatef(0, -0.4, 0)
        glScalef(0.12, 0.5, 0.12)
        draw_box((1,1,1), color=(0.2,0.2,0.2))
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0, -0.6, -0.15)
        glRotatef(-leg_rot, 1, 0, 0)
        glTranslatef(0, -0.4, 0)
        glScalef(0.12, 0.5, 0.12)
        draw_box((1,1,1), color=(0.2,0.2,0.2))
        glPopMatrix()
        glPopMatrix()

class EnemyCar:
    def __init__(self, z_start):
        self.is_aggressive = random.random() < 0.3
        self.color = (0.8, 0, 0) if self.is_aggressive else (random.random(), random.random(), random.random())
        self.lane = random.choice(['RIGHT', 'LEFT', 'RIGHT', 'RIGHT'])
        if self.lane == 'RIGHT': 
            self.x = 4.5
            self.direction = 1
            self.speed = random.uniform(0.6, 0.9) if self.is_aggressive else random.uniform(0.4, 0.6)
            self.rot_base = 180
        else: 
            self.x = -4.5
            self.direction = -1
            self.speed = random.uniform(0.4, 0.6) if self.is_aggressive else random.uniform(0.2, 0.4)
            self.rot_base = 0
            
        self.z = z_start
        self.cur_speed = self.speed
        self.turn = 0
        self.target_x = self.x
        self.braking = False

    def update(self, lights):
        min_d = 9999
        rel_l = None
        self.braking = False
        
        for tl in lights:
            dist = tl.z - self.z if self.direction == 1 else self.z - tl.z
            if 0 < dist < 120 and dist < min_d: 
                min_d = dist
                rel_l = tl
        
        should_stop = rel_l and rel_l.state in ["RED", "YELLOW"]
        approaching_intersection = rel_l and min_d < 60
        
        if (should_stop or approaching_intersection) and not self.is_aggressive:
            self.braking = True
            if should_stop and min_d < 25: 
                 self.cur_speed = max(0, self.cur_speed * 0.85) # Hard brake
            elif should_stop: 
                 self.cur_speed *= 0.97 # Normal brake
            else:
                 self.cur_speed *= 0.99 # Caution at intersection
        elif self.is_aggressive:
            if self.cur_speed < self.speed * 1.5: self.cur_speed += 0.01
            if random.random() < 0.05: self.target_x = self.x + random.choice([-1, 1])
        else: 
            if self.cur_speed < self.speed: self.cur_speed += 0.02

            
        self.z += self.cur_speed * self.direction
        dx = self.target_x - self.x
        self.x += dx * 0.1
        self.turn = -dx * 20

    def draw(self, is_night):
        glPushMatrix()
        glTranslatef(self.x, 0.8, self.z)
        glRotatef(self.rot_base + self.turn, 0, 1, 0)
        glPushMatrix()
        glScalef(1.1, 0.35, 2.2)
        draw_box((1,1,1), color=self.color)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0, 0.5, -0.2)
        glScalef(0.9, 0.3, 1.1)
        draw_box((1,1,1), color=(0.2,0.2,0.2))
        glPopMatrix()
        
        if is_night or self.braking: 
            emission = (1, 0, 0, 1) if self.braking else (1, 1, 0.5, 1) # Red if braking, Yellowish if normal night
            glMaterialfv(GL_FRONT, GL_EMISSION, emission)
            
        glPushMatrix(); glTranslatef(-0.7,0,-2.15); glScalef(0.2,0.1,0.1); draw_box((1,1,1), color=(1,0,0) if self.braking else (1,1,0.5)); glPopMatrix()
        glPushMatrix(); glTranslatef(0.7,0,-2.15); glScalef(0.2,0.1,0.1); draw_box((1,1,1), color=(1,0,0) if self.braking else (1,1,0.5)); glPopMatrix()
        glMaterialfv(GL_FRONT, GL_EMISSION, (0,0,0,1))
        
        for wx, wz in [(-1.1,-1.2),(1.1,-1.2),(-1.1,1.2),(1.1,1.2)]: 
            glPushMatrix()
            glTranslatef(wx,-0.35,wz)
            glScalef(0.3,0.3,0.3)
            draw_box((1,1,1), color=(0.1,0.1,0.1))
            glPopMatrix()
        glPopMatrix()

class PlayerCar:
    def __init__(self, audio):
        self.audio = audio; self.x = -4.5; self.z = 0; self.vel_x = 0; self.vel_z = 0; self.crashed = False; self.spin = 0; self.accel = 0.035; self.off_road = False
    def update(self, keys):
        if self.crashed: self.spin += 15; self.z += self.vel_z * 0.9; self.x += self.vel_x * 0.9; return
        mz = 0; mx = 0
        if keys[K_w]: mz = -1
        if keys[K_s]: mz = 1
        if keys[K_a]: mx = -1
        if keys[K_d]: mx = 1
        if keys[K_h]: self.audio.play("horn")
        self.vel_z += mz * self.accel; self.vel_x += mx * self.accel; self.vel_z *= 0.96; self.vel_x *= 0.96
        self.z += self.vel_z; self.x += self.vel_x
        if self.x > 9 or self.x < -9: self.off_road = True; self.vel_z *= 0.9
        else: self.off_road = False
    def draw(self, is_night):
        glPushMatrix()
        glTranslatef(self.x, 0.8, self.z)
        if self.crashed: glRotatef(self.spin, 0, 1, 0); glRotatef(20, 1, 0, 0)
        glRotatef(self.vel_x * -15, 0, 1, 0)
        glPushMatrix()
        glScalef(1.1, 0.35, 2.2)
        draw_box((1,1,1), color=(0.85, 0.1, 0.1))
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0, 0.5, -0.2)
        glScalef(0.9, 0.3, 1.1)
        draw_box((1,1,1), color=(0.1,0.1,0.1))
        glPopMatrix()
        
        ems = (1,1,0.8,1) if is_night else (0,0,0,1)
        glMaterialfv(GL_FRONT, GL_EMISSION, ems)
        glPushMatrix(); glTranslatef(-0.7,0,-2.15); glScalef(0.2,0.1,0.1); draw_box((1,1,1), color=(1,1,0.8)); glPopMatrix()
        glPushMatrix(); glTranslatef(0.7,0,-2.15); glScalef(0.2,0.1,0.1); draw_box((1,1,1), color=(1,1,0.8)); glPopMatrix()
        glMaterialfv(GL_FRONT, GL_EMISSION, (0,0,0,1))
        
        for wx, wz in [(-1.1,-1.2),(1.1,-1.2),(-1.1,1.2),(1.1,1.2)]: 
            glPushMatrix()
            glTranslatef(wx,-0.35,wz)
            glScalef(0.3,0.3,0.3)
            draw_box((1,1,1), color=(0.1,0.1,0.1))
            glPopMatrix()
        glPopMatrix()

class Environment:
    def draw(self, player_z, is_night):
        sl = 200; cs = int(player_z // sl)
        glPushMatrix()
        glTranslatef(0, -2, player_z - 450)
        random.seed(42)
        for _ in range(15): 
             mx = random.randint(-400, 400)
             if -50 < mx < 50: continue 
             glPushMatrix()
             glTranslatef(mx, random.randint(60,120)/2, random.randint(0,100))
             draw_pyramid_tex((60,100,60), "mountain", (0.5,0.5,0.5))
             glPopMatrix()
        glPopMatrix()
        
        for i in range(cs - 1, cs + 4):
            z_s = i * sl
            glPushMatrix()
            glTranslatef(0, 0, z_s)
            
            glPushMatrix()
            glTranslatef(0, -0.1, sl/2) 
            glScalef(10, 0.1, sl/2)
            draw_box((1,1,1), texture_name="asphalt", repeat_y=8)
            glPopMatrix()
            
            if is_night: glMaterialfv(GL_FRONT, GL_EMISSION, (0.5,0.5,0.5,1))
            glPushMatrix(); glTranslatef(-9.2, 0.02, sl/2); glScalef(0.25, 0.05, sl/2); draw_box((1,1,1), color=(1,1,1)); glPopMatrix()
            glPushMatrix(); glTranslatef(9.2, 0.02, sl/2); glScalef(0.25, 0.05, sl/2); draw_box((1,1,1), color=(1,1,1)); glPopMatrix()
            for d in range(int(sl/10)): 
                glPushMatrix()
                glTranslatef(0, 0.02, d*10+2)
                glScalef(0.2, 0.05, 2.0)
                draw_box((1,1,1), color=(1,1,1))
                glPopMatrix()
            glMaterialfv(GL_FRONT, GL_EMISSION, (0,0,0,1))
            
            glPushMatrix(); glTranslatef(-60, -0.5, sl/2); glScalef(50, 0.5, sl/2); draw_box((1,1,1), texture_name="grass", repeat_x=10, repeat_y=10); glPopMatrix()
            glPushMatrix(); glTranslatef(60, -0.5, sl/2); glScalef(50, 0.5, sl/2); draw_box((1,1,1), texture_name="grass", repeat_x=10, repeat_y=10); glPopMatrix()
            
            random.seed(i)
            for _ in range(15):
                glPushMatrix()
                glTranslatef(random.choice([-1,1])*random.randint(16, 55), 2.0, random.randint(0, sl))
                s = random.uniform(0.8, 1.5)
                glScalef(s, s, s)
                glRotatef(random.randint(0, 360), 0, 1, 0)
                draw_tree_realistic()
                glPopMatrix()
            glPopMatrix()

# --- MAIN ---
def main():
    pygame.init(); pygame.font.init()
    display = (WINDOW_WIDTH, WINDOW_HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption(GAME_TITLE)
    font = pygame.font.SysFont("Arial", 24)
    
    glViewport(0, 0, *display)
    glMatrixMode(GL_PROJECTION); glLoadIdentity(); gluPerspective(60, (display[0]/display[1]), 0.1, 1200.0)
    glMatrixMode(GL_MODELVIEW); glLoadIdentity()
    glEnable(GL_DEPTH_TEST); glEnable(GL_LIGHTING); glEnable(GL_LIGHT0); glEnable(GL_COLOR_MATERIAL)
    
    TextureManager.load_texture("asphalt", TextureManager.generate_surface(512, 512, "asphalt"))
    TextureManager.load_texture("grass", TextureManager.generate_surface(512, 512, "grass"))
    TextureManager.load_texture("mountain", TextureManager.generate_surface(256, 256, "mountain"))
    TextureManager.load_texture("bark", TextureManager.generate_surface(64, 256, "bark"))
    TextureManager.load_texture("leaf", TextureManager.generate_surface(256, 256, "leaf"))
    
    dn = DayNightSystem(); aud = AudioSystem(); p = PlayerCar(aud); env = Environment(); cam = Camera()
    traf = []; lits = []; peds = []; zc = []
    n_sp = -50; n_tl = -100
    
    clk = pygame.time.Clock(); run = True; msg = ""
    if aud.sounds.get("engine"): aud.sounds["engine"].play(loops=-1)

    while run:
        dt = clk.tick(FPS)
        for e in pygame.event.get(): 
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE): run = False
            if p.crashed and e.type == KEYDOWN and e.key == K_r:
                p = PlayerCar(aud); traf = []; lits = []; peds = []; zc = []
                n_sp = p.z - 200; n_tl = p.z - 300; msg = ""
            cam.process_event(e)
        
        dn.update(dt)
        p.update(pygame.key.get_pressed())
        
        if p.z < n_sp + 100: 
            traf.append(EnemyCar(n_sp - 200))
            n_sp -= random.randint(50, 150)
            
        if p.z < n_tl + 100: 
            z_pos = n_tl - 200
            lits.append(TrafficLight(z_pos))
            zc.append(ZebraCross(z_pos))
            n_tl -= random.randint(400, 800)
            for _ in range(random.randint(1,2)): 
                peds.append(Pedestrian(z_pos + random.uniform(-1,1)))

        if not p.crashed:
            for l in lits: l.update()
            for c in traf: c.update(lits)
            for pd in peds: pd.update()
            
            for c in traf: 
                if abs(p.x - c.x) < 2.5 and abs(p.z - c.z) < 4.0: 
                    p.crashed = True
                    aud.play("crash")
                    msg = "TABRAKAN MOBIL!"
            for l in lits:
                if abs(p.z - l.z) < 2.0 and l.state == "RED" and abs(p.vel_z) > 0.1: 
                    p.crashed = True
                    aud.play("horn")
                    msg = "LAMPU MERAH!"
            for pd in peds:
                if abs(p.x - pd.x) < 1.5 and abs(p.z - pd.z) < 1.5: 
                    p.crashed = True
                    aud.play("crash")
                    msg = "MENABRAK PEJALAN KAKI!"

        dn.apply()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        cam.apply((p.x, 0, p.z))
        
        is_n = dn.state == "MALAM"
        env.draw(p.z, is_n)
        for z in zc: z.draw(is_n)
        for l in lits: l.draw(is_n)
        for pd in peds: pd.draw()
        p.draw(is_n)
        for c in traf: c.draw(is_n)

        c_t = (dn.timer // 1000) % 180
        draw_text_on_screen(font.render(f"WAKTU: {dn.state}", True, (255,255,255)), 800, 20, 1024, 768)
        draw_text_on_screen(font.render(f"SPD: {int(abs(p.vel_z*100))}", True, (255,255,255)), 20, 20, 1024, 768)
        if p.crashed:
            draw_text_on_screen(font.render("GAME OVER", True, (255,0,0)), 450, 384, 1024, 768)
            draw_text_on_screen(font.render(msg, True, (255,255,0)), 400, 350, 1024, 768)
        elif p.off_road:
            draw_text_on_screen(font.render("AWAS! KELUAR JALUR!", True, (255, 100, 0)), 380, 600, 1024, 768)
        pygame.display.flip()
    pygame.quit()

class Camera:
    def __init__(self):
        self.distance = 35.0
        self.angle_y = 0.0
        self.angle_x = 25.0
        self.is_dragging = False
        self.last_pos = (0, 0)
        
    def process_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.is_dragging = True
                self.last_pos = pygame.mouse.get_pos()
            elif event.button == 4:
                self.distance = max(10.0, self.distance - 2.0)
            elif event.button == 5:
                self.distance = min(100.0, self.distance + 2.0)
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.is_dragging = False
        elif event.type == MOUSEMOTION:
            if self.is_dragging:
                mx, my = pygame.mouse.get_pos()
                dx = mx - self.last_pos[0]
                dy = my - self.last_pos[1]
                self.last_pos = (mx, my)
                self.angle_y += dx * 0.5
                self.angle_x += dy * 0.5
                self.angle_x = max(5, min(85, self.angle_x))

    def apply(self, t):
        rad_y = math.radians(self.angle_y)
        rad_x = math.radians(self.angle_x)
        
        dist_h = self.distance * math.cos(rad_x)
        y = self.distance * math.sin(rad_x)
        x = dist_h * math.sin(rad_y)
        z = dist_h * math.cos(rad_y)
        
        gluLookAt(t[0] + x, t[1] + y, t[2] + z, t[0], t[1] + 2.0, t[2], 0, 1, 0)

if __name__ == "__main__": main()
