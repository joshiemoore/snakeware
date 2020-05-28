import pygame
import math
import random


class Ball:
    def __init__(self, start_position):
        self.rect = pygame.Rect(start_position, (5, 5))
        self.colour = pygame.Color(255, 255, 255)
        self.position = [float(start_position[0]), float(start_position[1])]
        self.start_position = [self.position[0], self.position[1]]
        self.ball_speed = 120.0
        self.max_bat_bounce_angle = 5.0 * math.pi/12.0
        self.collided = False

        self.velocity = [0.0, 0.0]
        self.create_random_start_vector()

    def render(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)

    def create_random_start_vector(self):
        y_random = random.uniform(-0.5, 0.5)
        x_random = 1.0 - abs(y_random)
        if random.randint(0, 1) == 1:
            x_random = x_random * -1.0
        self.velocity = [x_random * self.ball_speed, y_random * self.ball_speed]

    def reset(self):
        self.position = [self.start_position[0], self.start_position[1]]
        self.create_random_start_vector()

    def update(self, dt, bats, walls):
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

        collided_this_frame = False
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                collided_this_frame = True
                if not self.collided:
                    self.collided = True
                    self.velocity[1] = self.velocity[1] * -1

        for bat in bats:
            if self.rect.colliderect(bat.rect):
                collided_this_frame = True
                if not self.collided:
                    self.collided = True
                    bat_y_centre = bat.position[1] + (bat.length/2)
                    ball_y_centre = self.position[1] + 5
                    relative_intersect_y = bat_y_centre - ball_y_centre  # should be in 'bat space' between -50 and +50
                    normalized_relative_intersect_y = relative_intersect_y/(bat.length/2)
                    bounce_angle = normalized_relative_intersect_y * self.max_bat_bounce_angle

                    self.velocity[0] = self.velocity[0] * -1
                    self.velocity[1] = self.ball_speed * -math.sin(bounce_angle)

        if not collided_this_frame:
            self.collided = False
