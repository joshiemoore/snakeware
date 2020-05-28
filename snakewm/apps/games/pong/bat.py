import pygame
from pygame.locals import *


class ControlScheme:
    def __init__(self):
        self.up = K_UP
        self.down = K_DOWN


class Bat:
    def __init__(self, start_pos, control_scheme, court_size):
        self.control_scheme = control_scheme
        self.move_up = False
        self.move_down = False
        self.move_speed = 450.0

        self.court_size = court_size

        self.length = 30.0
        self.width = 5.0

        self.position = [float(start_pos[0]), float(start_pos[1])]
        
        self.rect = pygame.Rect((start_pos[0], start_pos[1]), (self.width, self.length))
        self.colour = pygame.Color("#FFFFFF")

    def process_event(self, event):
        if event.type == KEYDOWN:
            if event.key == self.control_scheme.up:
                self.move_up = True
            if event.key == self.control_scheme.down:
                self.move_down = True

        if event.type == KEYUP:
            if event.key == self.control_scheme.up:
                self.move_up = False
            if event.key == self.control_scheme.down:
                self.move_down = False

    def update(self, dt):
        if self.move_up:
            self.position[1] -= dt * self.move_speed

            if self.position[1] < 10.0:
                self.position[1] = 10.0

            self.rect.y = self.position[1]
                
        if self.move_down:
            self.position[1] += dt * self.move_speed

            if self.position[1] > self.court_size[1] - self.length - 10:
                self.position[1] = self.court_size[1] - self.length - 10

            self.rect.y = self.position[1]

    def render(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)
