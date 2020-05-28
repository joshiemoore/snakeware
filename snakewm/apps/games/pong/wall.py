import pygame


class Wall:
    def __init__(self, top_left, bottom_right):
        self.rect = pygame.Rect(top_left, (bottom_right[0] - top_left[0], bottom_right[1] - top_left[1]))
        self.colour = pygame.Color("#C8C8C8")

    def render(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)
