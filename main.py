import pygame
import sys
import random

pygame.init()

# Fenstergröße
WIDTH, HEIGHT = 800, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Side-Scroller")

# Farben
WHITE = (255, 255, 255)

# Clock & FPS
clock = pygame.time.Clock()
FPS = 60

# Physik
GRAVITY = 0.8
JUMP_POWER = 15

# Bodenhöhe
GROUND_HEIGHT = 64
GROUND_Y = HEIGHT - GROUND_HEIGHT

# Spielergröße
PLAYER_WIDTH = 64
PLAYER_HEIGHT = 96

# Zombiegröße
ZOMBIE_WIDTH = 64
ZOMBIE_HEIGHT = 128

# Spielerposition
player_x = 100
player_y = GROUND_Y - PLAYER_HEIGHT
player_vel_y = 0
player_speed = 5
on_ground = True

# Sprites laden und skalieren
player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

ground_img = pygame.image.load("assets/ground.png")
ground_img = pygame.transform.scale(ground_img, (WIDTH, GROUND_HEIGHT))

zombie_img = pygame.image.load("assets/zombie.png")
zombie_img = pygame.transform.scale(zombie_img, (ZOMBIE_WIDTH, ZOMBIE_HEIGHT))

# Zombie-Verwaltung
zombies = []
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 3000)  # alle 3 Sekunden spawnt ein Zombie

def spawn_zombie():
    zombie = {
        "x": WIDTH + random.randint(0, 200),
        "y": GROUND_Y - ZOMBIE_HEIGHT,
        "speed": random.randint(2, 4)
    }
    zombies.append(zombie)

def draw_window():
    win.fill(WHITE)

    # Boden
    win.blit(ground_img, (0, GROUND_Y))

    # Spieler
    win.blit(player_img, (player_x, player_y))

    # Zombies
    for zombie in zombies:
        win.blit(zombie_img, (zombie["x"], zombie["y"]))

    pygame.display.update()

def main():
    global player_x, player_y, player_vel_y, on_ground

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == SPAWN_EVENT:
                spawn_zombie()

        # Steuerung
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and on_ground:
            player_vel_y = -JUMP_POWER
            on_ground = False

        # Schwerkraft
        player_vel_y += GRAVITY
        player_y += player_vel_y

        # Kollision mit Boden
        if player_y + PLAYER_HEIGHT >= GROUND_Y:
            player_y = GROUND_Y - PLAYER_HEIGHT
            player_vel_y = 0
            on_ground = True

        # Bildschirmgrenzen
        player_x = max(0, min(WIDTH - PLAYER_WIDTH, player_x))

        # Zombies bewegen
        for zombie in zombies[:]:
            zombie["x"] -= zombie["speed"]
            if zombie["x"] < -ZOMBIE_WIDTH:
                zombies.remove(zombie)

        # Fenster zeichnen
        draw_window()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
