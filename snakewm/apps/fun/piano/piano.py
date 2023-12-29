#!/usr/bin/env python

# Toy piano and Simon/Atari Touch Me game in PyGame

import os
import random
import time

import pygame
from pygame_gui.elements import UIWindow
from pygame_gui.elements.ui_image import UIImage


BLACK = 0, 0, 0
WHITE = 200, 200, 200
ORANGE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0
BACKGROUND = 33, 41, 46
GRAY = 76, 80, 82
LW = 10  # outline width
BKW = 22  # black key width
BKH = 200  # black key height
H = 350  # white key height
XADJ, YADJ = (
    16,
    40,
)  # shift needed due to window decoration when interpreting mouse position
bkeys = {1: 1, 2: 3, 4: 6, 5: 8, 6: 10}
wkeys = {0: 0, 1: 2, 2: 4, 3: 5, 4: 7, 5: 9, 6: 11, 7: 12}
RECT_NORMAL = pygame.Rect((236, 432, 130, 55))  # button rects
RECT_SIMON = pygame.Rect((400, 432, 150, 55))
RECT_VOL = pygame.Rect((25, 432, 200, 22))
RECT_OCT = pygame.Rect((570, 432, 210, 22))
NOTELEN = 0.6
SIMONCOL = (
    RED,
    ORANGE,
    GREEN,
    ORANGE,
    BLUE,
    ORANGE,
    ORANGE,
    YELLOW,
)  # colors when in Simon mode


class Piano(UIWindow):
    def __init__(self, pos, manager):
        self.res = 800, H + 150
        super().__init__(
            pygame.Rect(pos, (self.res[0] + 32, self.res[1] + 60)),
            manager=manager,
            window_display_title="piano",
            object_id="#piano",
            resizable=False,
        )

        self.dsurf = UIImage(
            pygame.Rect((0, 0), self.res),
            pygame.Surface(self.res).convert(),
            manager=manager,
            container=self,
            parent_element=self,
        )
        pygame.mixer.init()
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.volume = 5
        self.octave = 1
        self.sust = False
        self.load_inst()
        self.setvol()
        self.win = pygame.Surface(self.res)
        self.overlay = pygame.image.load(self.path + "/img/piano.png")
        self.keys = 13 * [False]
        self.playnote = None
        self.playtime = 0
        self.simon = False
        self.simonseq = []
        self.simonlen = 1
        self.simonplay = False
        self.simonstart = 0
        self.lastplayed = -1
        self.userseq = []

    def load_inst(self):
        "Load instrument samples"
        self.audio, self.sustain = {}, {}
        if self.octave == 0:
            o = "_low"
        elif self.octave == 2:
            o = "_high"
        else:
            o = ""
        for n in range(13):
            self.audio[n] = pygame.mixer.Sound(
                self.path + "/snd/piano%s_%02u.ogg" % (o, n)
            )
            self.sustain[n] = pygame.mixer.Sound(
                self.path + "/snd/piano%s_sustain_%02u.ogg" % (o, n)
            )
        self.audio["buzz"] = pygame.mixer.Sound(self.path + "/snd/buzz.ogg")
        self.setvol()

    def setvol(self):
        "Set volume for all loaded sounds"
        for n in range(13):
            self.audio[n].set_volume(self.volume / 10)
            self.sustain[n].set_volume(self.volume / 10)

    def setoct(self):
        "Change octave"
        self.load_inst()

    def process_event(self, event):
        super().process_event(event)
        r = super().get_abs_rect()
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x -= r[0] + XADJ
            y -= r[1] + YADJ
            p = self.pos2key(x, y)
            if p != None:
                self.play(p)
            if RECT_VOL.collidepoint(x, y):
                self.volume = int(1 + 10 * (x - RECT_VOL.left) / RECT_VOL.width)
                self.setvol()
            if RECT_OCT.collidepoint(x, y):
                self.octave = int(3 * (x - RECT_OCT.left) / RECT_VOL.width)
                self.setoct()
            if RECT_NORMAL.collidepoint(x, y) and self.simon:
                self.simon = False
                super().set_display_title("piano")
            if RECT_SIMON.collidepoint(x, y) and not self.simon:
                self.simon = True
                self.simonseq = [random.choice([0, 4, 7, 12]) for q in range(100)]
                self.simonlen = 1
                self.simonplay = True
                self.simonstart = time.time()
                super().set_display_title("simon")

        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            x -= r[0] + XADJ
            y -= r[1] + YADJ
            p = self.pos2key(x, y)
            if p != None:
                self.stop(p)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.stopall()

            if event.key == pygame.K_c:
                self.sust = not self.sust

            # volume
            if event.key == pygame.K_b:
                if self.volume < 10:
                    self.volume += 1
                self.setvol()
            if event.key == pygame.K_v:
                if self.volume > 1:
                    self.volume -= 1
                self.setvol()

            # octave
            if event.key == pygame.K_m:
                if self.octave < 2:
                    self.octave += 1
                self.setoct()
            if event.key == pygame.K_n:
                if self.octave > 0:
                    self.octave -= 1
                self.setoct()

            # piano key press
            if (
                event.key == pygame.K_s
                or event.key == pygame.K_1
                or event.key == pygame.K_LEFT
            ):
                self.play(0)
            if event.key == pygame.K_d:
                self.play(2)
            if (
                event.key == pygame.K_f
                or event.key == pygame.K_2
                or event.key == pygame.K_DOWN
            ):
                self.play(4)
            if event.key == pygame.K_g:
                self.play(5)
            if (
                event.key == pygame.K_h
                or event.key == pygame.K_3
                or event.key == pygame.K_RIGHT
            ):
                self.play(7)
            if event.key == pygame.K_j:
                self.play(9)
            if event.key == pygame.K_k:
                self.play(11)
            if (
                event.key == pygame.K_l
                or event.key == pygame.K_4
                or event.key == pygame.K_UP
            ):
                self.play(12)

            if event.key == pygame.K_e:
                self.play(1)
            if event.key == pygame.K_r:
                self.play(3)
            if (
                event.key == pygame.K_y or event.key == pygame.K_z
            ):  # QWERTY/QWERTZ layout
                self.play(6)
            if event.key == pygame.K_u:
                self.play(8)
            if event.key == pygame.K_i:
                self.play(10)

        # piano key release
        if event.type == pygame.KEYUP:
            if (
                event.key == pygame.K_s
                or event.key == pygame.K_1
                or event.key == pygame.K_LEFT
            ):
                self.stop(0)
            if event.key == pygame.K_d:
                self.stop(2)
            if (
                event.key == pygame.K_f
                or event.key == pygame.K_2
                or event.key == pygame.K_DOWN
            ):
                self.stop(4)
            if event.key == pygame.K_g:
                self.stop(5)
            if (
                event.key == pygame.K_h
                or event.key == pygame.K_3
                or event.key == pygame.K_RIGHT
            ):
                self.stop(7)
            if event.key == pygame.K_j:
                self.stop(9)
            if event.key == pygame.K_k:
                self.stop(11)
            if (
                event.key == pygame.K_l
                or event.key == pygame.K_4
                or event.key == pygame.K_UP
            ):
                self.stop(12)

            if event.key == pygame.K_e:
                self.stop(1)
            if event.key == pygame.K_r:
                self.stop(3)
            if (
                event.key == pygame.K_y or event.key == pygame.K_z
            ):  # QWERTY/QWERTZ layout
                self.stop(6)
            if event.key == pygame.K_u:
                self.stop(8)
            if event.key == pygame.K_i:
                self.stop(10)

    def play(self, k, user=True):
        "Play a note"
        self.audio[k].play()
        if user and self.sust:
            self.sustain[k].play(loops=-1)
        self.keys[k] = True

    def stop(self, k, user=True):
        "Stop playing a note"
        if self.sust:
            self.audio[k].stop()
        self.sustain[k].stop()
        self.keys[k] = False

        # check if user melody matches Simon's
        if self.simon and user == True:
            self.userseq.append(k)
            if self.userseq == self.simonseq[: self.simonlen]:
                print(self.simonlen, "CORRECT!")
                self.update(NOTELEN)
                time.sleep(NOTELEN)
                if self.simonlen < len(self.simonseq):
                    self.simonlen += 1
                self.simonplay = True
                self.simonstart = time.time()
                super().set_display_title(
                    "Simon (%u notes correct)" % (self.simonlen - 1)
                )
            if (
                self.userseq
                and self.userseq[-1] != self.simonseq[len(self.userseq) - 1]
            ):
                print("WRONG!")
                self.audio["buzz"].play()
                self.update(NOTELEN)
                time.sleep(1.5)
                self.simonplay = True
                self.simonstart = time.time()
                self.userseq = []

    def stopall(self):
        "Stop all notes"
        for k in range(13):
            self.sustain[k].stop()
            self.keys[k] = False

    def draw_wkey(self, k, c):
        "Draw white key"
        pygame.draw.rect(self.win, BLACK, (100 * k, 0, 100, H))
        pygame.draw.rect(self.win, c, (int(100 * k + LW / 2), LW, 100 - LW, H - 2 * LW))

    def draw_bkey(self, k, c):
        "Draw black key"
        pygame.draw.rect(self.win, c, (100 * k - BKW, 0, 2 * BKW, BKH))

    def pos2key(self, x, y):
        "Get key number from mouse click position"
        for k in 1, 2, 4, 5, 6:
            if y < BKH and (100 * k - BKW < x < 100 * k + BKW):
                return bkeys[k]
        for k in range(8):
            if y < H and 100 * k < x < 100 * (k + 1):
                return wkeys[k]

    def update(self, delta):
        super().update(delta)
        # Simon plays its melody
        if self.simon and self.simonplay:
            f = ((time.time() - self.simonstart) / NOTELEN) % 1
            if f > 0.8:
                self.keys = 13 * [False]
            n = int((time.time() - self.simonstart) / NOTELEN)
            if n >= self.simonlen:
                self.simonplay = False
                self.simonstart = 0
                self.lastplayed = -1
                self.userseq = []
            elif n > self.lastplayed:
                self.stopall()
                self.play(self.simonseq[n], user=False)
                self.lastplayed = n

        # draw keyboard
        self.win.fill(BACKGROUND)
        for k in range(8):
            c = WHITE
            for x in wkeys.keys():
                if x == k and self.keys[wkeys[x]]:
                    if self.simon:
                        c = SIMONCOL[k]
                    else:
                        c = ORANGE
            self.draw_wkey(k, c)
        for k in 1, 2, 4, 5, 6:
            c = BLACK
            for x in bkeys.keys():
                if x == k and self.keys[bkeys[x]]:
                    c = ORANGE
            self.draw_bkey(k, c)

        # draw buttons
        pygame.draw.rect(self.win, GRAY, RECT_NORMAL)
        pygame.draw.rect(self.win, GRAY, RECT_SIMON)
        if not self.simon:
            pygame.draw.rect(self.win, ORANGE, RECT_NORMAL, 3)
        else:
            pygame.draw.rect(self.win, ORANGE, RECT_SIMON, 3)

        # draw volume indicator
        for i in range(1, 11):
            if self.volume >= i:
                c = ORANGE
            else:
                c = GRAY
            pygame.draw.rect(self.win, c, (20 * i + 5, 432, 18, 22))

        # draw octave indicator
        for i in 0, 1, 2:
            if self.octave == i:
                c = ORANGE
            else:
                c = GRAY
            pygame.draw.rect(self.win, c, (70 * i + 570, 432, 65, 22))

        self.win.blit(self.overlay, (0, 0))

        self.dsurf.image.blit(self.win, (0, 0))
