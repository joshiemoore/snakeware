# Analog PyGame clock

import pygame
import pygame_gui
from pygame_gui.elements.ui_image import UIImage

from math import pi, cos, sin
import datetime


DARK = 33, 41, 46
WHITE = 255, 255, 255
GRAY = 76, 80, 82
RED = 255, 0, 0


class SnakeAClock(pygame_gui.elements.UIWindow):
    DIMS = (300, 300)

    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (self.DIMS[0] + 32, self.DIMS[1] + 60)),
            manager=manager,
            window_display_title="aclock",
            object_id="#aclock",
            resizable=True,
        )

        self.dsurf = UIImage(
            pygame.Rect((0, 0), self.DIMS),
            pygame.Surface(self.DIMS).convert(),
            manager=manager,
            container=self,
            parent_element=self,
        )
        self.draw_dial()
        self.clean_dial = self.dial.copy()
        self.manager = manager

    def process_event(self, event):
        super().process_event(event)
        r = super().get_abs_rect()
        if event.type == pygame.MOUSEBUTTONUP and (
            r.w != self.DIMS[0] + 32 or r.h != self.DIMS[1] + 60
        ):
            self.DIMS = r.w - 32, r.h - 60
            super().kill()
            self.__init__((r.left, r.top), self.manager)

    def update(self, delta):
        super().update(delta)
        self.dial = self.clean_dial.copy()
        self.draw_hands()
        self.dsurf.image.blit(self.dial, (0, 0))

    def clocksize(self):
        return int(0.95 * min(self.DIMS) / 2)

    def diam(self, x, r1, r2, r3, dx):
        x1, y1 = (
            r1 * self.clocksize() * sin(x * pi / 180),
            r1 * self.clocksize() * cos(x * pi / 180),
        )
        x2, y2 = (
            r2 * self.clocksize() * sin((x + dx) * pi / 180),
            r2 * self.clocksize() * cos((x + dx) * pi / 180),
        )
        x3, y3 = (
            r3 * self.clocksize() * sin(x * pi / 180),
            r3 * self.clocksize() * cos(x * pi / 180),
        )
        x4, y4 = (
            r2 * self.clocksize() * sin((x - dx) * pi / 180),
            r2 * self.clocksize() * cos((x - dx) * pi / 180),
        )
        p = [
            (int(x1 + self.DIMS[0] // 2), int(-y1 + self.DIMS[1] // 2)),
            (int(x2 + self.DIMS[0] // 2), int(-y2 + self.DIMS[1] // 2)),
            (int(x3 + self.DIMS[0] // 2), int(-y3 + self.DIMS[1] // 2)),
            (int(x4 + self.DIMS[0] // 2), int(-y4 + self.DIMS[1] // 2)),
        ]
        pygame.draw.polygon(self.dial, WHITE, p)

    def draw_dial(self):
        self.dial = pygame.Surface(self.DIMS)
        self.dial.fill(DARK)
        pygame.draw.circle(
            self.dial, WHITE, (self.DIMS[0] // 2, self.DIMS[1] // 2), self.clocksize()
        )
        pygame.draw.circle(
            self.dial,
            GRAY,
            (self.DIMS[0] // 2, self.DIMS[1] // 2),
            int(0.99 * self.clocksize()),
        )
        for x in range(60):
            if x % 5 == 0:
                continue
            x1, y1 = (
                0.95 * self.clocksize() * sin(6 * x * pi / 180),
                0.95 * self.clocksize() * cos(6 * x * pi / 180),
            )
            x2, y2 = (
                0.92 * self.clocksize() * sin(6 * x * pi / 180),
                0.92 * self.clocksize() * cos(6 * x * pi / 180),
            )
            pygame.draw.line(
                self.dial,
                WHITE,
                (int(x1 + self.DIMS[0] // 2), int(y1 + self.DIMS[1] // 2)),
                (int(x2 + self.DIMS[0] // 2), int(y2 + self.DIMS[1] // 2)),
                2,
            )
        for x in range(0, 360, 30):
            if x % 90 == 0:
                self.diam(x, 0.95, 0.88, 0.88, 2)
            else:
                self.diam(x, 0.95, 0.95, 0.87, 1)

    def draw_hands(self):
        # hour hand
        now = datetime.datetime.now()
        x = 30 * ((now.hour - 12) % 12) + now.minute / 2
        self.diam(x, 0.45, 0.08, -0.08, 30)

        # minute hand
        x = 6 * now.minute + now.second / 10
        self.diam(x, 0.75, 0.08, -0.08, 25)

        # second hand
        x = 6 * now.second
        x1, y1 = (
            0.8 * self.clocksize() * sin(x * pi / 180),
            0.8 * self.clocksize() * cos(x * pi / 180),
        )
        x2, y2 = 0, 0
        pygame.draw.line(
            self.dial,
            RED,
            (int(x1 + self.DIMS[0] // 2), int(-y1 + self.DIMS[1] // 2)),
            (int(x2 + self.DIMS[0] // 2), int(-y2 + self.DIMS[1] // 2)),
            3,
        )
