import pygame
import os
import random

pygame.init()
pygame.font.init()
pygame.mixer.init()

# === WINDOW SETUP ===
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Space Duel - Obat Rotasi")

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# BORDER
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

# FONTS
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# GAME CONSTANTS
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3

# size limits (px)
MIN_SIZE = 20
MAX_SIZE = 150

# EVENTS
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# === HELPER: load & scale image ===
def load_ship_image(path, w, h, rotate):
    img = pygame.image.load(os.path.join('Assets', path)).convert_alpha()
    img = pygame.transform.scale(img, (w, h))
    img = pygame.transform.rotate(img, rotate)
    return img

# === INITIAL SIZES & IMAGES ===
YELLOW_SIZE = 55
RED_SIZE = 55

YELLOW_SPACESHIP = load_ship_image('spaceship_yellow.png', YELLOW_SIZE, YELLOW_SIZE, 90)
RED_SPACESHIP = load_ship_image('spaceship_red.png', RED_SIZE, RED_SIZE, 270)

SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets', 'space.png')).convert(),
    (WIDTH, HEIGHT)
)

# === OBAT: IMAGE + ROTATION SUPPORT ===
OBAT_IMG = pygame.image.load(os.path.join("Assets", "obat.png")).convert_alpha()
OBAT_SIZE = 40
OBAT_IMG = pygame.transform.scale(OBAT_IMG, (OBAT_SIZE, OBAT_SIZE))
obat_angle = 0   # rotation angle

obat_rect = None
obat_spawn_time = None
obat_timer = pygame.time.get_ticks() + random.randint(5000, 10000)

def spawn_obat():
    size = OBAT_SIZE
    x = random.randint(50, WIDTH - 50 - size)
    y = random.randint(50, HEIGHT - 50 - size)
    return pygame.Rect(x, y, size, size)

# === DRAW ===
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, obat_rect, obat_angle):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    # ROTATING OBAT
    if obat_rect is not None:
        rotated = pygame.transform.rotate(OBAT_IMG, obat_angle)
        new_rect = rotated.get_rect(center=obat_rect.center)
        WIN.blit(rotated, new_rect.topleft)

    pygame.display.update()

# === MOVEMENTS ===
def yellow_handle_movement(keys, yellow):
    if keys[pygame.K_a] and yellow.x - VEL > 0:
        yellow.x -= VEL
    if keys[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
        yellow.x += VEL
    if keys[pygame.K_w] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT:
        yellow.y += VEL

def red_handle_movement(keys, red):
    if keys[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    if keys[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL
    if keys[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if keys[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT:
        red.y += VEL

# === SCALING ===
def scale_ship(current_size, amount, image_path, rotate_degree):
    new_size = max(MIN_SIZE, min(MAX_SIZE, current_size + amount))
    new_image = load_ship_image(image_path, new_size, new_size, rotate_degree)
    return new_size, new_image

# === BULLETS ===
def handle_bullets(yellow_bullets, red_bullets, yellow_rect, red_rect):
    for bullet in yellow_bullets[:]:
        bullet.x += BULLET_VEL
        if red_rect.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets[:]:
        bullet.x -= BULLET_VEL
        if yellow_rect.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

# === WINNER ===
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text,
             (WIDTH/2 - draw_text.get_width()/2,
              HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

# === MAIN GAME ===
def main():
    global YELLOW_SPACESHIP, RED_SPACESHIP, YELLOW_SIZE, RED_SIZE
    global obat_rect, obat_timer, obat_spawn_time

    red = pygame.Rect(700, 300, RED_SIZE, RED_SIZE)
    yellow = pygame.Rect(100, 300, YELLOW_SIZE, YELLOW_SIZE)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    obat_angle = 0

    while run:
        clock.tick(FPS)
        now = pygame.time.get_ticks()

        # ROTATE OBAT CONTINUOUSLY
        obat_angle = (obat_angle + 3) % 360

        # Spawn obat
        if obat_rect is None and now >= obat_timer:
            obat_rect = spawn_obat()
            obat_spawn_time = now

        # Auto-remove obat after 15s
        if obat_rect is not None and now - obat_spawn_time > 15000:
            obat_rect = None
            obat_timer = now + random.randint(5000, 10000)

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width,
                                         yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x,
                                         red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)

            # HIT EVENTS
            if event.type == RED_HIT:
                red_health -= 1
                YELLOW_SIZE, YELLOW_SPACESHIP = scale_ship(YELLOW_SIZE, +10, "spaceship_yellow.png", 90)
                RED_SIZE, RED_SPACESHIP = scale_ship(RED_SIZE, -10, "spaceship_red.png", 270)

                red.width = red.height = RED_SIZE
                yellow.width = yellow.height = YELLOW_SIZE

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                RED_SIZE, RED_SPACESHIP = scale_ship(RED_SIZE, +10, "spaceship_red.png", 270)
                YELLOW_SIZE, YELLOW_SPACESHIP = scale_ship(YELLOW_SIZE, -10, "spaceship_yellow.png", 90)

                red.width = red.height = RED_SIZE
                yellow.width = yellow.height = YELLOW_SIZE

        # WINNER
        if red_health <= 0:
            draw_winner("Yellow Wins!")
            break
        if yellow_health <= 0:
            draw_winner("Red Wins!")
            break

        keys = pygame.key.get_pressed()
        yellow_handle_movement(keys, yellow)
        red_handle_movement(keys, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        # OBAT PICKUP
        if obat_rect is not None:
            if yellow.colliderect(obat_rect):
                YELLOW_SIZE, YELLOW_SPACESHIP = scale_ship(YELLOW_SIZE, +15, "spaceship_yellow.png", 90)
                yellow.width = yellow.height = YELLOW_SIZE
                obat_rect = None
                obat_timer = now + random.randint(5000, 10000)

            elif red.colliderect(obat_rect):
                RED_SIZE, RED_SPACESHIP = scale_ship(RED_SIZE, +15, "spaceship_red.png", 270)
                red.width = red.height = RED_SIZE
                obat_rect = None
                obat_timer = now + random.randint(5000, 10000)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health, obat_rect, obat_angle)

    pygame.quit()

if __name__ == "__main__":
    main()
