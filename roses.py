import pygame
import random
import math

# --------------------------------------------------
# 8-particle iterated map from 1986 EXE
# --------------------------------------------------

WIDTH = 640
HEIGHT = 350

SCALE = 9.5
CENTER_X = 320
CENTER_Y = 223

# EGA colors 8..15
EGA = [
    (85, 85, 85),      # 8
    (85, 85, 255),     # 9
    (85, 255, 85),     # 10
    (85, 255, 255),    # 11
    (255, 85, 85),     # 12
    (255, 85, 255),    # 13
    (255, 255, 85),    # 14
    (255, 255, 255),   # 15
]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8-Particle Rose Attractor")

surface = pygame.Surface((WIDTH, HEIGHT))
surface.fill((0, 0, 0))

# random parameter
a = random.uniform(-1.0, 1.0)
b = 1.0 - a

print(f"a = {a:.6f}")
print(f"b = {b:.6f}")

particles = []

# initial conditions
for i in range(8):
    t = 2.0 * i - 0.51
    x = t
    y = t
    c = 2.0 * b * x * x / (1.0 + x * x)

    particles.append({
        "x": x,
        "y": y,
        "c": c,
        "color": EGA[i]
    })

clock = pygame.time.Clock()
running = True

ITERATIONS_PER_FRAME = 200

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # perform many iterations each frame
    for _ in range(ITERATIONS_PER_FRAME):

        for p in particles:

            x = p["x"]
            y = p["y"]
            c = p["c"]

            # map iteration
            xp = a * x + y + c

            cp = 2.0 * b * xp * xp / (1.0 + xp * xp)

            yp = a * xp - x + cp

            p["x"] = xp
            p["y"] = yp
            p["c"] = cp

            px = int(SCALE * xp + CENTER_X)
            py = int(SCALE * yp + CENTER_Y)

            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                surface.set_at((px, py), p["color"])

    screen.blit(surface, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
