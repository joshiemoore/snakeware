"""
Snake Window Manager
"""

TESTMODE = __name__ == "__main__"

import os
import sys
import importlib

import pygame, pygame_gui

if TESTMODE:
    from appmenu.appmenupanel import AppMenuPanel

    from snakebg.bg import SnakeBG
    from snakebg.bgmenu import SnakeBGMenu
else:
    from snakewm.appmenu.appmenupanel import AppMenuPanel

    from snakewm.snakebg.bg import SnakeBG
    from snakewm.snakebg.bgmenu import SnakeBGMenu


class SnakeWM:
    SCREEN = None
    DIMS = None
    BG = None
    MANAGER = None

    BG_COLOR = (0, 128, 128)

    # background color paint properties
    PAINT = False
    PAINT_RADIUS = 10

    # 16 color palette
    PAINT_COLOR = 0
    PAINT_COLOR_LIST = [
        (255, 255, 255),
        (192, 192, 192),
        (128, 128, 128),
        (0, 0, 0),
        (0, 255, 0),
        (0, 128, 0),
        (128, 128, 0),
        (0, 128, 128),
        (255, 0, 0),
        (128, 0, 0),
        (128, 0, 128),
        (255, 0, 255),
        (0, 0, 255),
        (0, 0, 128),
        (0, 255, 255),
        (255, 255, 0),
    ]

    # paint shapes
    PAINT_SHAPE = 0
    NUM_SHAPES = 3

    # reference to SnakeBG object for dynamic backgrounds
    DYNBG = None
    DYNBG_MENU = None

    # currently focused window
    FOCUS = None

    # dict that will contain the apps directory structure
    APPS = {}
    # reference to the root app menu object
    APPMENU = None

    def __init__(self):
        # populate the apps tree
        apps_path = os.path.dirname(os.path.abspath(__file__)) + "/apps"
        SnakeWM.iter_dir(self.APPS, apps_path)

        pygame.init()

        # initialize pygame to framebuffer
        os.putenv("SDL_FBDEV", "/dev/fb0")
        pygame.display.init()

        # get screen dimensions
        self.DIMS = (pygame.display.Info().current_w, pygame.display.Info().current_h)

        # init screen
        self.SCREEN = pygame.display.set_mode(self.DIMS, pygame.FULLSCREEN)

        # init background
        self.BG = pygame.Surface((self.DIMS))
        self.BG.fill(self.BG_COLOR)

        self.BRUSH_SURF = pygame.Surface((self.DIMS), flags=pygame.SRCALPHA)
        self.BRUSH_SURF.fill((0, 0, 0, 0))

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
            if os.path.isfile(path + "/" + f + "/__init__.py"):
                tree[f] = None
            elif os.path.isdir(path + "/" + f):
                tree[f] = {}
                SnakeWM.iter_dir(tree[f], path + "/" + f)

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
        if not TESTMODE:
            app = "snakewm." + app

        _app = importlib.import_module(app)

        try:
            _app.load(self.MANAGER, params)
        except:
            pygame.quit()

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
        self.BG = pygame.Surface((self.DIMS))
        self.BG_COLOR = color
        self.BG.fill(self.BG_COLOR)

    def set_bg_image(self, file):
        """
        Sets the desktop background to an image.
        """
        filename, file_extension = os.path.splitext(file)
        if file_extension == ".jpg" or file_extension == ".png":
            self.BG = pygame.transform.scale(pygame.image.load(file), self.DIMS)

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
                                "apps",
                                self.APPS,
                                self.appmenu_load,
                            )
                        else:
                            # close app menu
                            self.APPMENU.destroy()
                            self.APPMENU = None

                    if pressed[pygame.K_LALT]:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            pygame.quit()
                            exit()
                        elif event.key == pygame.K_p:
                            # toggle paint mode
                            self.PAINT = not self.PAINT
                            self.BRUSH_SURF.fill((0, 0, 0, 0))
                        elif event.key == pygame.K_d:
                            # toggle dynamic background
                            if self.DYNBG is None and self.DYNBG_MENU is None:
                                self.DYNBG_MENU = SnakeBGMenu(self.MANAGER)
                            elif self.DYNBG is not None:
                                del self.DYNBG
                                self.DYNBG = None

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.PAINT:
                        if event.button == 4:
                            # mouse wheel up
                            if pressed[pygame.K_LALT]:
                                self.PAINT_COLOR = (self.PAINT_COLOR + 1) % len(
                                    self.PAINT_COLOR_LIST
                                )
                            elif pressed[pygame.K_LCTRL]:
                                self.PAINT_SHAPE = (
                                    self.PAINT_SHAPE + 1
                                ) % self.NUM_SHAPES
                            else:
                                self.PAINT_RADIUS += 2
                        elif event.button == 5:
                            # mouse wheel down
                            if pressed[pygame.K_LALT]:
                                self.PAINT_COLOR = (self.PAINT_COLOR - 1) % len(
                                    self.PAINT_COLOR_LIST
                                )
                            elif pressed[pygame.K_LCTRL]:
                                self.PAINT_SHAPE = (
                                    self.PAINT_SHAPE - 1
                                ) % self.NUM_SHAPES
                            else:
                                self.PAINT_RADIUS -= 2
                            if self.PAINT_RADIUS < 2:
                                self.PAINT_RADIUS = 2
                elif event.type == pygame.USEREVENT:
                    if event.user_type == "window_selected":
                        # focus selected window
                        if self.FOCUS is not None:
                            self.FOCUS.unfocus()
                        self.FOCUS = event.ui_element
                        self.FOCUS.focus()
                    elif event.user_type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                        if event.ui_object_id == "#desktop_colour_picker":
                            # set desktop background color - no alpha channel
                            self.set_bg_color(event.colour[:-1])
                    elif event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                        if event.ui_object_id == "#background_picker":
                            self.set_bg_image(event.text)
                    elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if "#bgmenu" in event.ui_object_id:
                            if "close_button" in event.ui_object_id:
                                self.DYNBG_MENU.kill()
                                del self.DYNBG_MENU
                                self.DYNBG_MENU = None
                            elif not "title_bar" in event.ui_object_id:
                                selected_bg = event.ui_object_id.split(".")[1]
                                self.DYNBG = SnakeBG(selected_bg, TESTMODE)
                                self.DYNBG_MENU.kill()
                                del self.DYNBG_MENU
                                self.DYNBG_MENU = None

                                self.PAINT = False

                self.MANAGER.process_events(event)

            self.MANAGER.update(delta)

            # blit paintbrush/dynbg layer
            if self.DYNBG is not None:
                # update dynamic background
                self.DYNBG.draw(self.BRUSH_SURF)
                self.SCREEN.blit(self.BG, (0, 0))
                self.SCREEN.blit(self.BRUSH_SURF, (0, 0))
            elif self.PAINT:
                mpos = pygame.mouse.get_pos()

                # default drawing the brush to the temporary brush layer
                draw_surf = self.BRUSH_SURF

                if pygame.mouse.get_pressed()[0]:
                    # paint to the actual background
                    draw_surf = self.BG

                if self.PAINT_SHAPE == 0:
                    # circle
                    pygame.draw.circle(
                        draw_surf,
                        self.PAINT_COLOR_LIST[self.PAINT_COLOR],
                        mpos,
                        self.PAINT_RADIUS,
                    )
                elif self.PAINT_SHAPE == 1:
                    # square
                    pygame.draw.rect(
                        draw_surf,
                        self.PAINT_COLOR_LIST[self.PAINT_COLOR],
                        pygame.Rect(
                            (mpos[0] - self.PAINT_RADIUS, mpos[1] - self.PAINT_RADIUS),
                            (self.PAINT_RADIUS * 2, self.PAINT_RADIUS * 2),
                        ),
                    )
                elif self.PAINT_SHAPE == 2:
                    # triangle
                    pygame.draw.polygon(
                        draw_surf,
                        self.PAINT_COLOR_LIST[self.PAINT_COLOR],
                        (
                            (mpos[0] - self.PAINT_RADIUS, mpos[1] + self.PAINT_RADIUS),
                            (mpos[0] + self.PAINT_RADIUS, mpos[1] + self.PAINT_RADIUS),
                            (mpos[0], mpos[1] - self.PAINT_RADIUS),
                        ),
                    )

                self.SCREEN.blit(self.BG, (0, 0))
                self.SCREEN.blit(self.BRUSH_SURF, (0, 0))
                self.BRUSH_SURF.fill((0, 0, 0, 0))
            else:
                # not in paint mode, just blit background
                self.SCREEN.blit(self.BG, (0, 0))

            self.MANAGER.draw_ui(self.SCREEN)
            pygame.display.update()


if TESTMODE:
    wm = SnakeWM()
    wm.run()
