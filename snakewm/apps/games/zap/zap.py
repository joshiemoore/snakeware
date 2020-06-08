# Zap

import pygame
import pygame_gui
from pygame_gui.elements.ui_image import UIImage

from math import sin, cos, pi
import random, time, os

RES = 160  # horizontal resolution
RESY = int(0.75 * RES)
RES2 = RES / 2
CENTER = int(RES2), int(0.75 * RES2)
SRES = 800  # initial upscaled horizontal resolution (window can be resized)
SSIZ = 10  # station size
ENSIZ = 4  # enemy size
PSIZ = 2  # photon torpedo size
SATSIZ = 3  # attack satellite size
PI2 = pi / 2
BASES = 3  # initial numbers of bases
NEWBASE = 75000  # score for a bonus base


class Zap(pygame_gui.elements.UIWindow):
    res = SRES, int(0.75 * SRES)

    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (self.res[0] + 32, self.res[1] + 60)),
            manager=manager,
            window_display_title="zap",
            object_id="#zap",
            resizable=True,
        )

        self.dsurf = UIImage(
            pygame.Rect((0, 0), self.res),
            pygame.Surface(self.res).convert(),
            manager=manager,
            container=self,
            parent_element=self,
        )
        self.dazz = pygame.Surface((RES, RESY))
        self.paused = False
        self.step = False
        self.dir = 0
        self.hiscore = 0
        self.phot = [1000, 1000, 1000, 1000]
        self.newgame()
        pygame.mixer.init()
        path = os.path.dirname(os.path.abspath(__file__))
        self.audio = {
            "fanfare": pygame.mixer.Sound(path + "/snd/fanfare.ogg"),
            "start": pygame.mixer.Sound(path + "/snd/start.ogg"),
            "fire": pygame.mixer.Sound(path + "/snd/shot.ogg"),
            "shiphit": pygame.mixer.Sound(path + "/snd/enemy.ogg"),
            "end": pygame.mixer.Sound(path + "/snd/stationdest.ogg"),
            "pfire": pygame.mixer.Sound(path + "/snd/photon.ogg"),
            "pdest": pygame.mixer.Sound(path + "/snd/photondest.ogg"),
            "satdest": pygame.mixer.Sound(path + "/snd/sat.ogg"),
        }
        self.img = {
            "station": pygame.image.load(path + "/img/station.png"),
            "photon": pygame.image.load(path + "/img/photon.png"),
            "fighter2": pygame.image.load(path + "/img/fighter.png"),
            "sat": pygame.image.load(path + "/img/satellite.png"),
            "num": pygame.image.load(path + "/img/numbers.png"),
            "text": pygame.image.load(path + "/img/text.png"),
        }
        self.img["fighter1"] = pygame.transform.rotate(self.img["fighter2"], 90)
        self.img["fighter0"] = pygame.transform.rotate(self.img["fighter2"], 180)
        self.img["fighter3"] = pygame.transform.rotate(self.img["fighter2"], 270)
        self.attractimg = pygame.image.load(path + "/img/title.png")
        self.audio["fanfare"].play()
        self.attract = True
        self.manager = manager

    def newgame(self):
        "Set up a new game, reset everthing"
        self.shipdir = random.randint(0, 3)
        self.shipdist = 100
        self.score = 0
        self.bonus = 0
        self.phot = [1000, 1000, 1000, 1000]
        self.lastshot = time.time()
        self.bases = BASES
        self.lasertime = 0
        self.satstage = False
        self.satdir, self.satdist = 0, 1000
        self.starfield = pygame.Surface((RES, RESY))
        self.starfield.fill((0, 0, 0))
        for n in range(200):
            x, y = random.randint(0, RES - 1), random.randint(0, RESY - 1)
            pygame.draw.line(self.starfield, (120, 120, 120), (x, y), (x, y))

    def process_event(self, event):
        super().process_event(event)
        r = super().get_abs_rect()
        if event.type == pygame.MOUSEBUTTONUP and (
            r.w != self.res[0] + 32 or r.h != self.res[1] + 60
        ):
            self.res = r.w - 32, r.h - 60
            super().kill()
            self.__init__((r.left, r.top), self.manager)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            self.paused = not self.paused
        if event.type == pygame.KEYDOWN and event.key == pygame.K_PERIOD:
            self.step = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self.attract:
                self.attract = False
                self.audio["start"].play()
                time.sleep(1)
            else:
                self.fire()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            self.dir = 0
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            self.dir = 1
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            self.dir = 2
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            self.dir = 3

    def incscore(self, x):
        "Increase score and highscore"
        self.score += x
        self.hiscore = max(self.score, self.hiscore)
        print("S/HS", self.score, self.hiscore)
        self.bonus = self.score // NEWBASE
        print(self.bases + self.bonus, "BASES")

    def fire(self):
        "Trigger has been pulled, check if anything has been hit"
        self.audio["fire"].play()
        self.lasertime = time.time()
        if self.satstage:
            if abs(self.dir - (self.satdir % 4)) < 0.25:
                self.incscore(2000)
                self.audio["satdest"].play()
                self.satstage = False
                self.satdir, self.satdist = 0, 1000
                return
            else:
                return

        if (
            self.dir == self.shipdir
            and self.shipdist < 1000
            and self.shipdist < self.phot[self.dir]
        ):
            self.incscore(500)
            self.audio["shiphit"].play()
            if random.random() < 0.1:
                self.satstage = True
                self.satdist = 100
                self.satdir = random.uniform(0, 4)
                self.shipdist = 100
                print("ATTACK SATELLITE!")
            else:
                self.shipdist = 100
                self.shipdir = random.randint(0, 3)
            return
        if self.phot[self.dir] < 1000:
            self.incscore(250)
            self.audio["pdest"].play()
            self.phot[self.dir] = 1000
            return

    def station(self, s):
        "Draw the station"
        self.dazz.blit(self.img["station"], (CENTER[0] - s, CENTER[1] - s))

    def enemy(self, s):
        "Draw enemy fighters"
        x, y = (
            int(self.shipdist * sin(PI2 * self.shipdir)),
            int(self.shipdist * cos(PI2 * self.shipdir)),
        )
        self.dazz.blit(
            self.img["fighter%u" % self.shipdir], (CENTER[0] - s + x, CENTER[1] - s - y)
        )

    def photons(self, s):
        "Draw photon torpedoes"
        for n in range(4):
            x, y = (int(self.phot[n] * sin(PI2 * n)), int(self.phot[n] * cos(PI2 * n)))
            self.dazz.blit(self.img["photon"], (CENTER[0] - s + x, CENTER[1] - s - y))

    def sat(self, s):
        "Draw attack satellite"
        x, y = (
            int(self.satdist * sin(PI2 * self.satdir)),
            int(self.satdist * cos(PI2 * self.satdir)),
        )
        self.dazz.blit(self.img["sat"], (CENTER[0] - s + x, CENTER[1] - s - y))

    def gun(self):
        "Draw the station's gun"
        pygame.draw.line(
            self.dazz,
            (255, 255, 0),
            (CENTER[0], CENTER[1]),
            (
                int(CENTER[0] + 1.5 * SSIZ * sin(PI2 * self.dir)),
                int(CENTER[1] - 1.5 * SSIZ * cos(PI2 * self.dir)),
            ),
        )

    def laser(self):
        "Draw a laser shot from the station"
        dist = min(100, self.shipdist, self.phot[self.dir])
        if time.time() - self.lasertime < 0.1:
            pygame.draw.line(
                self.dazz,
                (255, 255, 255),
                (CENTER[0], CENTER[1]),
                (
                    int(CENTER[0] + dist * sin(PI2 * self.dir)),
                    int(CENTER[1] - dist * cos(PI2 * self.dir)),
                ),
            )

    def scores(self):
        "Draw score and highscore display"
        for n, c in enumerate("%u" % self.score):
            i = int(c)
            self.dazz.blit(self.img["num"], (5 * n, 6), area=(5 * i, 0, 5, 5))
        dx = RES - 5 * len("%u" % self.hiscore) + 1
        for n, c in enumerate("%u" % self.hiscore):
            i = int(c)
            self.dazz.blit(self.img["num"], (5 * n + dx, 6), area=(5 * i, 0, 5, 5))
        for n, c in enumerate("%u" % (self.bases + self.bonus)):
            i = int(c)
            self.dazz.blit(self.img["num"], (5 * n, RESY - 11), area=(5 * i, 0, 5, 5))

        self.dazz.blit(self.img["text"], (RES - 28, 0), area=(0, 0, 28, 5))
        self.dazz.blit(self.img["text"], (0, 0), area=(7, 0, 28, 5))
        self.dazz.blit(self.img["text"], (0, RESY - 5), area=(0, 6, 28, 5))

    def endgame(self):
        "The station has been destroyed"
        self.bases -= 1
        print(self.bases + self.bonus, "BASES")
        if self.bases + self.bonus > 0:
            self.audio["shiphit"].play(loops=5)
            time.sleep(4)
            self.shipdist = 100
            self.shipdir = random.randint(0, 3)
            self.phot = [1000, 1000, 1000, 1000]
            self.lastshot = time.time()
            self.satstage = False
            self.lasertime = 0
        else:
            self.audio["shiphit"].play(loops=8)
            time.sleep(6)
            self.newgame()
            self.attract = True

    def update(self, delta):
        super().update(delta)
        "Main loop"
        if self.paused and not self.step:
            return
        self.step = False

        if self.attract:  # title screen
            out = pygame.transform.scale(self.attractimg, (self.res))
            self.dsurf.image.blit(out, (0, 0))
            return

        if self.satstage:  # killer satellite active?
            self.satdir += 0.02
            self.satdist -= 0.2
            if self.satdist < SSIZ:
                self.endgame()
        else:  # normal play
            self.shipdist -= 0.5
            for n in range(4):
                if self.phot[n] < 1000:
                    self.phot[n] -= 1
                if self.phot[n] == 1000 and self.shipdir == n:
                    if time.time() - self.lastshot > 1:
                        self.phot[n] = self.shipdist - 1
                        self.lastshot = time.time()
                        self.audio["pfire"].play()
                        if random.random() < 0.3:
                            self.shipdist = 100
                            self.shipdir = random.randint(0, 3)
            if (self.shipdist < SSIZ + ENSIZ) or (min(self.phot) < SSIZ + PSIZ):
                self.endgame()
        self.dazz.blit(self.starfield, (0, 0))
        self.laser()
        self.station(SSIZ)
        if self.satstage:
            self.sat(SATSIZ)
        else:
            self.enemy(ENSIZ)
            self.photons(PSIZ)
        self.gun()
        self.scores()
        out = pygame.transform.scale(self.dazz, (self.res))

        self.dsurf.image.blit(out, (0, 0))
