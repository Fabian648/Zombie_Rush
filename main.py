import pygame
import sys

# Pygame initialisieren
pygame.init()

# Fenstergröße
WIDTH, HEIGHT = 800, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side-Scroller mit Sprung")

# Farben
WHITE = (255, 255, 255)

# FPS und Clock
FPS = 60
clock = pygame.time.Clock()

# Physik
GRAVITY = 0.8
JUMP_POWER = 15

# Spieler-Parameter
player_pos_x = 100
player_pos_y = 0
player_speed = 5
player_width = 50
player_height = 70

player_vel_y = 0
on_ground = False

# Bodenhöhe (y-Koordinate)
GROUND_LEVEL = HEIGHT - 50

# Grafiken laden
player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (player_width, player_height))

ground_img = pygame.image.load("assets/ground.png")
ground_img = pygame.transform.scale(ground_img, (WIDTH, 50))

def draw():
    win.fill(WHITE)
    # Boden zeichnen
    win.blit(ground_img, (0, GROUND_LEVEL))

    # Spieler zeichnen
    win.blit(player_img, (player_pos_x, player_pos_y))

    pygame.display.update()

def main():
    global player_pos_x, player_pos_y, player_vel_y, on_ground

    running = True
    player_pos_y = GROUND_LEVEL - player_height  # Start auf dem Boden

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        # Links/Rechts Bewegung
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_pos_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_pos_x += player_speed

        # Springen
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and on_ground:
            player_vel_y = -JUMP_POWER
            on_ground = False

        # Schwerkraft anwenden
        player_vel_y += GRAVITY
        player_pos_y += player_vel_y

        # Boden Kollision
        if player_pos_y + player_height >= GROUND_LEVEL:
            player_pos_y = GROUND_LEVEL - player_height
            player_vel_y = 0
            on_ground = True

        # Spielfeld Begrenzung horizontal
        player_pos_x = max(0, min(WIDTH - player_width, player_pos_x))

        draw()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
