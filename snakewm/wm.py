"""
Snake Window Manager
"""

import os
import sys
import importlib

import pygame, pygame_gui

from appmenu.appmenupanel import AppMenuPanel

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

        ## REMOVE ME
        AppMenuPanel(
            self.MANAGER,
            (0, 0),
            'apps',
            {
              'test': {
                'HelloWorld': None,
                'asdf': {
                  'cool': None,
                  'wow': None
                },
                'a': None,
                'b': None
              },
              'games': {
                'pong': None
              }
            }
        )
        ##

        pygame.mouse.set_visible(True)
        pygame.display.update()

    def loadapp(self, app, params=None):
        """
        Load and run a Python module as an app (ie "apps.test.HelloWorld").
        Apps are basically just Python packages. The loaded app package must
        contain an __init__.py with a load() function that accepts a UIManager
        parameter and a params list parameter.

        The load() function should create an instance of the app to load and
        add the app UI to the passed UIManager object. See existing apps for 
        examples.
        """
        if __name__ != '__main__':
            app = 'snakewm.' + app

        _app = importlib.import_module(app)
        _app.load(self.MANAGER, params)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            delta = clock.tick(60) / 1000.0

            pressed = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                     if pressed[pygame.K_LALT]:
                         if event.key == pygame.K_ESCAPE:
                             running = False
                         elif event.key == pygame.K_h:
                             self.loadapp("apps.test.HelloWorld")
                         elif event.key == pygame.K_p:
                             self.loadapp("apps.games.pong")

                self.MANAGER.process_events(event)

            self.MANAGER.update(delta)

            self.SCREEN.blit(self.BG, (0, 0))
            self.MANAGER.draw_ui(self.SCREEN)
            pygame.display.update()

if __name__ == '__main__':
    wm = SnakeWM()
    wm.run()
