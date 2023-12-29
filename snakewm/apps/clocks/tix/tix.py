#!/usr/bin/env python

"""
Displays the TIX clock
2011-01-08 / 2020-06-12
"""

# Usage: tix.py [update interval] [--24]

import random
import sys
import time

import pygame
from pygame_gui.elements import UIWindow
from pygame_gui.elements.ui_image import UIImage

try:
    inter = int(sys.argv[1])
except:
    inter = 4  # default update interval (secs)

RED = 204, 0, 0
GREEN = 78, 154, 6
BLUE = 52, 101, 164
BACKGROUND = 33, 41, 46
GRAY = 76, 80, 82
COL = (BACKGROUND, BACKGROUND, GRAY, RED, GREEN, BLUE)

if "--24" in sys.argv:
    f = "%H%M"
else:
    f = "%I%M"


def tog(start, end, n, col=2):
    """Toggle on n values randomly in the array between start and end"""

    global disp

    for z in random.sample(range(3 * (end - start)), n):
        disp[z % 3][start + z // 3] = col


def mainprog(win, res):
    """Main prog"""

    global disp

    boxx, boxy = res[0] // 12, res[0] // 12

    t = time.strftime(f, time.localtime())
    h1, h2, m1, m2 = [int(x) for x in t]
    disp = [[2, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2] for _ in range(3)]
    tog(0, 1, h1, 3)
    tog(2, 5, h2, 4)
    tog(6, 8, m1, 5)
    tog(9, 12, m2, 3)
    for x in range(12):
        for y in range(3):
            pygame.draw.rect(
                win, COL[disp[y][x]], [x * boxx + 1, y * boxy + 1, boxx - 2, boxy - 2]
            )


class TIX(UIWindow):
    """TIX"""

    res = 420, 105

    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (self.res[0] + 32, self.res[1] + 60)),
            manager=manager,
            window_display_title="tix",
            object_id="#tix",
            resizable=True,
        )

        self.dsurf = UIImage(
            pygame.Rect((0, 0), self.res),
            pygame.Surface(self.res).convert(),
            manager=manager,
            container=self,
            parent_element=self,
        )
        self.screen = pygame.Surface(self.res)
        self.screen.fill(BACKGROUND)
        self.manager = manager
        self.last = 0

    def process_event(self, event):
        """Process event"""

        super().process_event(event)
        r = super().get_abs_rect()
        if event.type == pygame.MOUSEBUTTONUP and (
            r.w != self.res[0] + 32 or r.h != self.res[1] + 60
        ):
            self.res = r.w - 32, r.h - 60
            super().kill()
            self.__init__((r.left, r.top), self.manager)

    def update(self, delta):
        """Update"""

        super().update(delta)
        if time.time() - self.last < inter:
            return
        self.last = time.time()
        self.screen.fill(BACKGROUND)
        mainprog(self.screen, self.res)
        self.dsurf.image.blit(self.screen, (0, 0))
