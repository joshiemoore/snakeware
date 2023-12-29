"""
A simple little demo app for snakeware, it draws circles.

Josh Moore 2020
"""

import os
import random

import pygame
from pygame.locals import FULLSCREEN, KEYDOWN, K_ESCAPE


class CirclezApp:
    """Circlez App"""

    def __init__(self):
        pygame.init()

        # set pygame to fbdev mode
        os.putenv("SDL_FBDEV", "/dev/fb0")
        pygame.display.init()

        # get screen dimensions
        self.DIMS = (pygame.display.Info().current_w, pygame.display.Info().current_h)

        # init screen
        self.SCREEN = pygame.display.set_mode(self.DIMS, FULLSCREEN)

        # init background
        self.BG = pygame.Surface((self.DIMS))
        self.BG.fill((0, 0, 0))

        pygame.mouse.set_visible(False)
        pygame.display.update()

    def run(self):
        """Run Circlez App"""

        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    exit()

            pygame.draw.circle(
                self.BG,
                (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                ),
                (random.randint(0, self.DIMS[0]), random.randint(0, self.DIMS[1])),
                random.randint(10, 100),
            )
            self.SCREEN.blit(self.BG, (0, 0))
            pygame.display.flip()
            clock.tick(30)
