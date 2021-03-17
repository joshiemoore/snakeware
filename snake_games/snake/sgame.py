from pygame.locals import *
from random import randint
import pygame
import time
import os


class Apple:
    x = 0
    y = 0
    step = 44

    def __init__(self, x, y):
        self.x = x * self.step
        self.y = y * self.step

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), (self.x, self.y, 44, 44), 0)


class Player:
    x = [0]
    y = [0]
    step = 44
    direction = 0
    length = 3

    updateCountMax = 2
    updateCount = 0

    def __init__(self, length):
        self.length = length
        for i in range(0, 2000):
            self.x.append(-100)
            self.y.append(-100)

        # initial positions, no collision.
        self.x[1] = 1 * 44
        self.x[2] = 2 * 44

    def update(self):

        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:

            # update previous positions
            for i in range(self.length - 1, 0, -1):
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]

            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step

            self.updateCount = 0

    def moveRight(self):
        self.direction = 0

    def moveLeft(self):
        self.direction = 1

    def moveUp(self):
        self.direction = 2

    def moveDown(self):
        self.direction = 3

    def draw(self, surface):
        for i in range(0, self.length):
            pygame.draw.rect(surface, (255, 0, 0), (self.x[i], self.y[i], 44, 44), 0)


class Game:
    def isCollision(self, x1, y1, x2, y2, bsize):
        if x1 >= x2 and x1 <= x2 + bsize:
            if y1 >= y2 and y1 <= y2 + bsize:
                return True
        return False


class SnakeApp:
    player = 0
    apple = 0

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.game = Game()
        self.player = Player(3)
        self.apple = Apple(5, 5)

    def on_init(self):
        pygame.init()

        # initialize pygame to the framebuffer
        os.putenv("SDL_FBDEV", "/dev/fb0")
        pygame.display.init()
        pygame.mouse.set_visible(False)

        self.DIMS = (pygame.display.Info().current_w, pygame.display.Info().current_h)

        self._display_surf = pygame.display.set_mode(self.DIMS, pygame.FULLSCREEN)

        self._running = True

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self.player.update()

        # does snake eat apple?
        for i in range(0, self.player.length):
            if self.game.isCollision(
                self.apple.x, self.apple.y, self.player.x[i], self.player.y[i], 44
            ):
                self.apple.x = randint(2, int(self.DIMS[0] / 44) - 2) * 44
                self.apple.y = randint(2, int(self.DIMS[1] / 44) - 2) * 44
                self.player.length = self.player.length + 1

        # does snake collide with itself?
        for i in range(2, self.player.length):
            if self.game.isCollision(
                self.player.x[0],
                self.player.y[0],
                self.player.x[i],
                self.player.y[i],
                40,
            ):
                print("You lose! Collision: ")
                print(
                    "x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")"
                )
                print(
                    "x["
                    + str(i)
                    + "] ("
                    + str(self.player.x[i])
                    + ","
                    + str(self.player.y[i])
                    + ")"
                )
                self._running = False

        # is the snake out of bounds?
        if (
            self.player.x[0] < 0
            or self.player.y[0] < 0
            or self.player.x[0] >= self.DIMS[0]
            or self.player.y[0] >= self.DIMS[1]
        ):
            print("You lose!")
            self._running = False
    def on_render(self):
        self._display_surf.fill((0, 0, 0))
        self.player.draw(self._display_surf)
        self.apple.draw(self._display_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
        exit(0)

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_RIGHT]:
                self.player.moveRight()

            if keys[K_LEFT]:
                self.player.moveLeft()

            if keys[K_UP]:
                self.player.moveUp()

            if keys[K_DOWN]:
                self.player.moveDown()

            if keys[K_ESCAPE]:
                self._running = False

            self.on_loop()
            self.on_render()

            time.sleep(50.0 / 1000.0)
        self.on_cleanup()
