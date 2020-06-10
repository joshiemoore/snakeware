#!/usr/bin/env python

# Toy piano and Simon/Atari Touch Me game in PyGame

import pygame
import pygame_gui
from pygame_gui.elements.ui_image import UIImage

import os, time, random

BLACK = 0, 0, 0
WHITE = 200, 200, 200
ORANGE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0
BACKGROUND = 33, 41, 46
GRAY = 76, 80, 82
LW = 10        # outline width
BKW = 22       # black key width
BKH = 200      # black key height
H = 350        # white key height
bkeys = {1: 1, 2: 3, 4: 6, 5: 8, 6: 10}
wkeys = {0: 0, 1: 2, 2: 4, 3: 5, 4: 7, 5: 9, 6: 11, 7: 12}
RECT_NORMAL = pygame.Rect((236, 432, 130, 55))  # button rects
RECT_SIMON = pygame.Rect((400, 432, 150, 55))
NOTELEN = 0.6
SIMONCOL = (RED, ORANGE, GREEN, ORANGE, BLUE, ORANGE, ORANGE, YELLOW)  # colors when in Simon mode

class Piano(pygame_gui.elements.UIWindow):
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
        self.win = pygame.Surface(self.res)
        self.audio = {}
        path = os.path.dirname(os.path.abspath(__file__))
        for n in range(13):
            self.audio[n] = pygame.mixer.Sound(path + "/snd/piano_%02u.ogg" % n)
        self.audio["buzz"] = pygame.mixer.Sound(path + "/snd/buzz.ogg")
        self.overlay = pygame.image.load(path + "/img/piano.png")
        self.playnote = None
        self.playtime = 0
        self.simon = False
        self.simonseq = []
        self.simonlen = 1
        self.simonplay = False
        self.simonstart = 0
        self.lastplayed = -1
        self.userseq = []

    def process_event(self, event):
        super().process_event(event)
        r = super().get_abs_rect()
        if event.type == pygame.QUIT: self.running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            x -= r[0] + 16
            y -= r[1] + 40
            p = self.pos2key(x,y)
            if p != None:
                self.play(p)
            if RECT_NORMAL.collidepoint(x, y) and self.simon:
                self.simon = False
                super().set_display_title('piano')
            if RECT_SIMON.collidepoint(x, y) and not self.simon:
                self.simon = True
                self.simonseq = [random.choice([0, 4, 7, 12]) for q in range(100)]
                self.simonlen = 1
                self.simonplay = True
                self.simonstart = time.time()
                super().set_display_title('simon')
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s or event.key == pygame.K_1 or event.key == pygame.K_LEFT:
                self.play(0)
            if event.key == pygame.K_d:
                self.play(2)
            if event.key == pygame.K_f or event.key == pygame.K_2 or event.key == pygame.K_DOWN:
                self.play(4)
            if event.key == pygame.K_g:
                self.play(5)
            if event.key == pygame.K_h or event.key == pygame.K_3 or event.key == pygame.K_RIGHT:
                self.play(7)
            if event.key == pygame.K_j:
                self.play(9)
            if event.key == pygame.K_k:
                self.play(11)
            if event.key == pygame.K_l or event.key == pygame.K_4 or event.key == pygame.K_UP:
                self.play(12)

            if event.key == pygame.K_e:
                self.play(1)
            if event.key == pygame.K_r:
                self.play(3)
            if event.key == pygame.K_y or event.key == pygame.K_z:  # QWERTY/QWERTZ layout
                self.play(6)
            if event.key == pygame.K_u:
                self.play(8)
            if event.key == pygame.K_i:
                self.play(10)

    def play(self, k, user = True):
        "Play a note"
        self.audio[k].play()
        self.playnote = k
        self.playtime = time.time()
        if self.simon and user == True:
            self.userseq.append(k)
            if self.userseq == self.simonseq[:self.simonlen]:
                print(self.simonlen, "CORRECT!")
                self.update(NOTELEN)
                time.sleep(NOTELEN)
                self.playnote = None
                self.update(NOTELEN)
                time.sleep(NOTELEN)
                if self.simonlen < len(self.simonseq):
                    self.simonlen += 1
                self.simonplay = True
                self.simonstart = time.time()
                super().set_display_title('simon (%u notes correct)' % (self.simonlen - 1))
            if self.userseq and self.userseq[-1] != self.simonseq[len(self.userseq) - 1]:
                print("WRONG!")
                time.sleep(NOTELEN)
                self.audio["buzz"].play()
                time.sleep(.8)
                self.simonplay = True
                self.simonstart = time.time()
                self.userseq = []

    def draw_wkey(self, k, c):
        "Draw white key"
        pygame.draw.rect(self.win, BLACK, (100*k, 0, 100, H))
        pygame.draw.rect(self.win, c, (int(100*k+LW/2), LW, 100-LW, H-2*LW))

    def draw_bkey(self, k, c):
        "Draw black key"
        pygame.draw.rect(self.win, c, (100*k-BKW, 0, 2*BKW, BKH))

    def pos2key(self, x, y):
        "Get key num from mouse click position"
        for k in 1, 2, 4, 5, 6:
            if y < BKH and (100*k-BKW < x < 100*k+BKW):
                return bkeys[k]
        for k in range(8):
            if y < H and 100*k < x < 100*(k+1):
                return wkeys[k]

    def update(self, delta):
        super().update(delta)
        if self.simon and self.simonplay:
            n = int((time.time() - self.simonstart) / NOTELEN)
            if n >= self.simonlen:
                self.simonplay = False
                self.simonstart = 0
                self.lastplayed = -1
                self.userseq = []
            elif n > self.lastplayed:
                self.play(self.simonseq[n], user = False)
                self.lastplayed = n
        self.win.fill(BACKGROUND)
        if not self.simon:
            if time.time() - self.playtime > 0.2:
                self.playnote = None
        else:
            if time.time() - self.playtime > .85 * NOTELEN:
                self.playnote = None
        for k in range(8):
            c = WHITE
            for x in wkeys.keys():
                if x == k and wkeys[x] == self.playnote:
                    if self.simon:
                        c = SIMONCOL[k]
                    else:
                        c = ORANGE
            self.draw_wkey(k, c)
        for k in 1, 2, 4, 5, 6:
            c = BLACK
            for x in bkeys.keys():
                if x == k and bkeys[x] == self.playnote:
                    c = ORANGE
            self.draw_bkey(k, c)

        pygame.draw.rect(self.win, GRAY, RECT_NORMAL)
        pygame.draw.rect(self.win, GRAY, RECT_SIMON)
        if not self.simon:
            pygame.draw.rect(self.win, ORANGE, RECT_NORMAL, 3)
        else:
            pygame.draw.rect(self.win, ORANGE, RECT_SIMON, 3)
        self.win.blit(self.overlay, (0, 0))

        self.dsurf.image.blit(self.win, (0, 0))

