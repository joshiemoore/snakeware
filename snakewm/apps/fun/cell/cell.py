#!/usr/bin/env python

"""Cellular automaton"""

import random

import pygame
from pygame_gui.elements import UIWindow
from pygame_gui.elements.ui_image import UIImage

RULES = (
    18,
    22,
    26,
    30,
    41,
    45,
    54,
    60,
    90,
    102,
    105,
    106,
    110,
    122,
    126,
    146,
    150,
    154,
    182,
)
RES = 300, 500
NCELL = RES[0]


def getcol():
    """Get col"""

    return [85 * random.randint(0, 3) for _ in range(3)]


class Cell(UIWindow):
    """Cell"""

    DIMS = RES

    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (self.DIMS[0] + 32, self.DIMS[1] + 60)),
            manager=manager,
            window_display_title="cell",
            object_id="#cell",
            resizable=True,
        )

        self.dsurf = UIImage(
            pygame.Rect((0, 0), self.DIMS),
            pygame.Surface(self.DIMS).convert(),
            manager=manager,
            container=self,
            parent_element=self,
        )
        self.screen = pygame.Surface(self.DIMS)
        self.manager = manager
        self.cell = [random.randint(0, 1) for _ in range(2 + NCELL)]
        self.rule = random.choice(RULES)
        self.gen = 1
        self.line = 0
        self.COL = getcol(), getcol()

    def process_event(self, event):
        """Process event"""

        super().process_event(event)
        r = super().get_abs_rect()
        if event.type == pygame.MOUSEBUTTONUP and (
            r.w != self.DIMS[0] + 32 or r.h != self.DIMS[1] + 60
        ):
            self.DIMS = r.w - 32, r.h - 60
            super().kill()
            self.__init__((r.left, r.top), self.manager)

    def newgen(self):
        """New gen"""

        self.gen += 1
        cell2 = [0 for _ in range(2 + NCELL)]
        for x in range(NCELL):
            s = 2 ** (4 * self.cell[x] + 2 * self.cell[x + 1] + self.cell[x + 2])
            if s & self.rule:
                cell2[x + 1] = 1
        # make cyclic
        cell2[0] = cell2[-2]
        cell2[-1] = cell2[1]
        self.cell = cell2

    def update(self, delta):
        """Update"""

        super().update(delta)
        self.line += 1
        self.screen.scroll(dy=-1)
        pygame.draw.line(
            self.screen,
            (0, 0, 0),
            (0, self.DIMS[1] - 1),
            (self.DIMS[0] - 1, self.DIMS[1] - 1),
            1,
        )
        scrollfac = max(1, int(self.DIMS[0] / RES[0]))
        if self.line % scrollfac == 0:
            self.newgen()
        for x in range(self.DIMS[0]):
            xp = int(x / self.DIMS[0] * NCELL)
            pygame.draw.line(
                self.screen,
                self.COL[self.cell[xp + 1]],
                (x, self.DIMS[1] - 1),
                (x, self.DIMS[1] - 1),
                1,
            )
        super().set_display_title("cell (rule %u)" % self.rule)
        self.dsurf.image.blit(self.screen, (0, 0))
