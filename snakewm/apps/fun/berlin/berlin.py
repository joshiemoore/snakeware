#!/usr/bin/env python

# Displays the Berlin clock
# 2020-06-13

import pygame
import pygame_gui
from pygame_gui.elements.ui_image import UIImage

import sys, time, datetime

ORANGE = 204, 100, 0
YELLOW = 249, 244, 46
BACKGROUND = 33, 41, 46
GRAY = 76, 80, 82
BORDER = 1
RES = 220,250
inter = 1

def mainprog(win, res):
    global disp

    box4, box11, boxy = res[0] // 4, res[0] // 11, res[1] // 5

    now = datetime.datetime.now()
    for x in range(4):
        h1, h2 = divmod(now.hour, 5)
        mm = now.minute % 5
        if x < h1: c1 = ORANGE
        else: c1 = GRAY
        if x < h2: c2 = ORANGE
        else: c2 = GRAY
        if x < mm: c3 = YELLOW
        else: c3 = GRAY
        pygame.draw.rect(win, c1, [x * box4 + BORDER, boxy + BORDER,
            box4 - 2 * BORDER, boxy - 2 * BORDER])
        pygame.draw.rect(win, c2, [x * box4 + BORDER, 2 * boxy + BORDER,
            box4 - 2 * BORDER, boxy - 2 * BORDER])
        pygame.draw.rect(win, c3, [x * box4 + BORDER, 4 * boxy + BORDER,
            box4 - 2 * BORDER, boxy - 2 * BORDER])
    for x in range(11):
        m5 = now.minute // 5
        if x < m5:
            if (x + 1) % 3 == 0: c = ORANGE
            else: c = YELLOW
        else: c = GRAY
        pygame.draw.rect(win, c, [x * box11 + BORDER, 3 * boxy + BORDER,
            box11 - 2 * BORDER, boxy - 2 * BORDER])
    if now.second % 2 == 0: c = YELLOW
    else: c = GRAY
    pygame.draw.circle(win, c, (2 * box4, boxy // 2), boxy // 2 - BORDER)


class Berlin(pygame_gui.elements.UIWindow):
    res = RES

    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (self.res[0] + 32, self.res[1] + 60)),
            manager=manager,
            window_display_title="berlin",
            object_id="#berlin",
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
        super().process_event(event)
        r = super().get_abs_rect()
        if event.type == pygame.MOUSEBUTTONUP and (
            r.w != self.res[0] + 32 or r.h != self.res[1] + 60
        ):
            self.res = r.w - 32, r.h - 60
            super().kill()
            self.__init__((r.left, r.top), self.manager)

    def update(self, delta):
        super().update(delta)
        if time.time() - self.last < inter:
            return
        self.last = time.time()
        self.screen.fill(BACKGROUND)
        mainprog(self.screen, self.res)
        self.dsurf.image.blit(self.screen, (0, 0))
