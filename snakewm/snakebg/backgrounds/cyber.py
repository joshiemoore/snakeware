"""
Cyberpunk/synthwave-style dynamic background for SnakeBG

Joshua Moore 2020
"""

import math
import random

import pygame


# horizontal line offsets for "scrolling effect"
CYBER_OFFS = 0

# list of tuples containing star information
# (x, y, radius)
CYBER_STARS = None

# horizontal position of the ship
CYBER_SHIP_X = 200


def drawbg(surface):
    """Draw background"""

    global CYBER_OFFS
    global CYBER_STARS
    global CYBER_SHIP_X

    SURF_WIDTH = surface.get_width()
    SURF_HEIGHT = surface.get_height()

    # generate stars if needed
    if CYBER_STARS is None:
        CYBER_STARS = []
        for _ in range(50, 100):
            CYBER_STARS.append(
                (
                    random.randint(0, SURF_WIDTH),
                    random.randint(0, SURF_HEIGHT / 2 - 5),
                    random.randint(1, 4),
                )
            )

    surface.fill((0, 0, 0))

    # draw horizon line
    pygame.draw.line(
        surface, (255, 0, 255), (0, SURF_HEIGHT / 2), (SURF_WIDTH, SURF_HEIGHT / 2)
    )

    # draw vertical lines
    for theta in range(0, 180, 6):
        tdeg = math.radians(theta)
        pygame.draw.line(
            surface,
            (255, 0, 255),
            (SURF_WIDTH / 2, SURF_HEIGHT / 2),
            (
                SURF_WIDTH / 2 + math.cos(tdeg) * 2000,
                SURF_HEIGHT / 2 + math.sin(tdeg) * 2000,
            ),
        )

    # draw horizontal lines
    y = (SURF_HEIGHT / 2) - 20
    dy = 1
    while y <= SURF_HEIGHT:
        ty = y + CYBER_OFFS * (dy / 10)
        if ty > SURF_HEIGHT / 2:
            pygame.draw.line(surface, (255, 0, 255), (0, ty), (SURF_WIDTH, ty))

        y += dy
        dy += 5

    CYBER_OFFS += 0.1
    if CYBER_OFFS > 10:
        CYBER_OFFS = 0

    # draw ship
    draw_ship(
        surface, (int(SURF_WIDTH / 2), int(SURF_HEIGHT / 2)), CYBER_SHIP_X / SURF_WIDTH
    )

    CYBER_SHIP_X -= int((CYBER_SHIP_X - pygame.mouse.get_pos()[0]) / 50)

    # draw stars
    for star in CYBER_STARS:
        pygame.draw.circle(surface, (0, 255, 255), (star[0], star[1]), star[2])

    # draw sun
    pygame.draw.arc(
        surface,
        (255, 0, 255),
        pygame.Rect(SURF_WIDTH / 2 - 150, SURF_HEIGHT / 2 - 150, 300, 300),
        0,
        math.radians(181),
        2,
    )


def draw_ship(surface, origin, dx):
    """
    Draw the "spaceship"
    origin - tuple representing center of the screen
    dx - (shipX / screen_width)
    """
    fx = (
        origin[0] - int(math.cos(math.radians(dx * 180)) * 700),
        origin[1] + int(math.sin(math.radians(dx * 180)) * 300),
    )

    fl = (
        origin[0] - int(math.cos(math.radians((dx - 0.05) * 180)) * 700),
        origin[1] + int(math.sin(math.radians((dx - 0.1) * 180)) * 500),
    )

    fr = (
        origin[0] - int(math.cos(math.radians((dx + 0.05) * 180)) * 700),
        origin[1] + int(math.sin(math.radians((dx + 0.1) * 180)) * 500),
    )

    pygame.draw.polygon(surface, (0, 255, 255), (fx, fl, fr), 12)
