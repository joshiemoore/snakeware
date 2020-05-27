"""
Snake Window Manager
"""

import os
import sys

import pygame, pygame_gui

BG_COLOR = (0, 128, 128)

class SnakeWM:
    SCREEN = None
    DIMS = None
    BG = None
    MANAGER = None

    def __init__(self):
        pygame.init()

        # initialize pygame to framebuffer
        os.putenv('SDL_FBDEV', '/dev/fb0')
        pygame.display.init()

        # get screen dimensions
        self.DIMS = (
            pygame.display.Info().current_w,
            pygame.display.Info().current_h
        )

        # init screen
        self.SCREEN = pygame.display.set_mode(
            self.DIMS,
            pygame.FULLSCREEN
        )

        # init background
        self.BG = pygame.Surface((self.DIMS))
        self.BG.fill(BG_COLOR)

        # init UI manager
        self.MANAGER = pygame_gui.UIManager(self.DIMS)

        pygame.mouse.set_visible(True)
        pygame.display.update()

    def alert(self, title, msg, pos):
        pygame_gui.windows.UIMessageWindow(
            rect=pygame.Rect(pos, (300, 160)),
            window_title=title,
            html_message=msg,
            manager=self.MANAGER
        )

    def run(self):
        clock = pygame.time.Clock()
        running = True

        self.alert('Test', 'Hello World!', (100, 100))
        self.alert('lol', 'It just werks', (500, 500))

        while running:
            delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_ESCAPE:
                         running = False

                self.MANAGER.process_events(event)

            self.MANAGER.update(delta)

            self.SCREEN.blit(self.BG, (0, 0))
            self.MANAGER.draw_ui(self.SCREEN)
            pygame.display.update()

if __name__ == '__main__':
    wm = SnakeWM()
    wm.run()
