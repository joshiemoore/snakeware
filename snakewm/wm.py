"""
Snake Window Manager
"""

import os
import sys
import importlib

import pygame, pygame_gui

from appmenu.appmenupanel import AppMenuPanel

class SnakeWM:
    SCREEN = None
    DIMS = None
    BG = None
    MANAGER = None

    BG_COLOR = (0, 128, 128)

    # currently focused window
    FOCUS = None

    # dict that will contain the apps directory structure
    APPS = {}
    # reference to the root app menu object
    APPMENU = None

    def __init__(self):
        # populate the apps tree
        apps_path = os.path.dirname(os.path.abspath(__file__)) + '/apps'
        SnakeWM.iter_dir(self.APPS, apps_path)

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
        self.BG.fill(self.BG_COLOR)

        # init UI manager
        self.MANAGER = pygame_gui.UIManager(self.DIMS)

        pygame.mouse.set_visible(True)
        pygame.display.update()


    def iter_dir(tree, path):
        """
        Static function that recursively populates dict 'tree' with the
        app directory structure starting at 'path'.
        """
        for f in os.listdir(path):
            if os.path.isfile(path + '/' + f + '/__init__.py'):
                tree[f] = None
            elif os.path.isdir(path + '/' + f):
                tree[f] = {}
                SnakeWM.iter_dir(tree[f], path + '/' + f)

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

    def appmenu_load(self, app):
        """
        This function is passed to AppMenuPanel objects to be called when
        an app is selected to be opened.
        The root app menu is destroyed, and the app is loaded.
        """
        if self.APPMENU is not None:
            self.APPMENU.destroy()
            self.APPMENU = None

        self.loadapp(app)

    def set_bg_color(self, color):
        """
        Set the desktop background to 'color', where color is an RGB tuple.
        """
        self.BG_COLOR = color
        self.BG.fill(self.BG_COLOR)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            delta = clock.tick(60) / 1000.0

            pressed = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_LSUPER:
                         if self.APPMENU is None:
                             # open app menu
                             self.APPMENU = AppMenuPanel(
                                 self.MANAGER,
                                 (0, 0),
                                 'apps',
                                 self.APPS,
                                 self.appmenu_load
                             )
                         else:
                             # close app menu
                             self.APPMENU.destroy()
                             self.APPMENU = None

                     if pressed[pygame.K_LALT]:
                         if event.key == pygame.K_ESCAPE:
                             running = False
                             return pygame.quit()

                elif event.type == pygame.USEREVENT:
                    if event.user_type == 'window_selected':
                        # focus selected window
                        if self.FOCUS is not None:
                            self.FOCUS.unfocus()
                        self.FOCUS = event.ui_element
                        self.FOCUS.focus()
                    elif event.user_type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                        if event.ui_object_id == '#desktop_colour_picker':
                            # set desktop background color - no alpha channel
                            self.set_bg_color(event.colour[:-1])

                self.MANAGER.process_events(event)

            self.MANAGER.update(delta)

            self.SCREEN.blit(self.BG, (0, 0))
            self.MANAGER.draw_ui(self.SCREEN)
            pygame.display.update()

if __name__ == '__main__':
    wm = SnakeWM()
    wm.run()
