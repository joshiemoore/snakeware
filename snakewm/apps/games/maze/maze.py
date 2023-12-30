"""Maze"""

import os
from random import random, randrange, shuffle

import pygame


class Maze:
    """Maze"""

    dirToDelta = {
        0: (0, -1),
        1: (1, 0),
        2: (0, 1),
        3: (-1, 0),
    }

    def __init__(self, size):

        app_path = os.path.dirname(os.path.abspath(__file__))
        assets_path = app_path + "/assets"

        self.size = size
        self.sprite_size = (32, 32)
        self.width = int(self.size[0] / self.sprite_size[0]) - 8
        self.height = int(self.size[1] / self.sprite_size[1]) - 2
        self.font_color = (255, 255, 255)
        self.font_bgcolor = (0, 0, 0)
        self.background = pygame.Surface(size)  # make a background surface
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        self.player = []
        self.player.append(pygame.image.load(assets_path + "/player_up.jpg").convert())
        self.player.append(
            pygame.image.load(assets_path + "/player_right.jpg").convert()
        )
        self.player.append(
            pygame.image.load(assets_path + "/player_down.jpg").convert()
        )
        self.player.append(
            pygame.image.load(assets_path + "/player_left.jpg").convert()
        )
        self.floor = []
        self.floor.append(pygame.image.load(assets_path + "/floor0.png").convert())
        self.floor.append(pygame.image.load(assets_path + "/floor1.png").convert())
        self.floor.append(pygame.image.load(assets_path + "/floor2.png").convert())
        self.wall = pygame.image.load(assets_path + "/wall.png").convert()

        self.font = pygame.font.Font(None, 24)
        self.font_height = self.font.size("")[1]
        self.font_xpos = (self.width + 2) * self.sprite_size[1]
        self.font_width = self.size[0] - self.font_xpos

        self.maze = [[-1 for _ in range(self.height)] for _ in range(self.width)]

        self.walls = self.height * self.width - 1
        self.moves = 0
        self.direction = 0
        self.x, self.y = randrange(self.width), randrange(self.height)

        self.maze[self.x][self.y] = 1
        self.visited = 1
        self.visited2 = 0
        self.unvisited = 0
        self.bumps = 0

        self.generate()

    def process_event(self, event):
        """Process event"""

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.turn(-1)
            elif event.key == pygame.K_RIGHT:
                self.turn()
            elif event.key == pygame.K_UP:
                self.move()
            else:
                return False
            return True
        return False

    def draw(self, surface):
        """Draw"""

        surface.blit(self.background, (0, 0))
        for y in range(-1, self.height + 1):
            self.draw_wall(surface, -1, y)
            self.draw_wall(surface, self.width, y)
        for x in range(-1, self.width + 1):
            self.draw_wall(surface, x, -1)
            self.draw_wall(surface, x, self.height)
        self.draw_stats_table(surface)
        for y in range(self.height):
            for x in range(self.width):
                if self.block_free((x, y)):
                    self.draw_empty(surface, x, y)
                else:
                    self.draw_wall(surface, x, y)
        self.draw_player(surface)

    def draw_wall(self, surface, x, y):
        """Draw wall"""

        rect = (
            ((x + 1) * self.sprite_size[0], (y + 1) * self.sprite_size[1]),
            (self.sprite_size),
        )
        surface.blit(self.wall, rect)

    def draw_empty(self, surface, x, y):
        """Draw empty"""

        rect = (
            ((x + 1) * self.sprite_size[0], (y + 1) * self.sprite_size[1]),
            (self.sprite_size),
        )
        surface.blit(self.floor[self.maze[x][y]], rect)

    def render_stats_text(self, surface, text, y):
        """Render stats text"""

        text = self.font.render(text, 1, self.font_color)
        textpos = text.get_rect()
        textpos.move_ip(self.font_xpos, y * self.font_height)
        textpos.width = self.font_width
        textpos.right
        surface.fill(self.font_bgcolor, textpos)
        surface.blit(text, textpos)

    def draw_player(self, surface):
        """Draw player"""

        rect = (
            ((self.x + 1) * self.sprite_size[0], (self.y + 1) * self.sprite_size[1]),
            (self.sprite_size),
        )
        surface.blit(self.player[self.direction], rect)

    def draw_stats_table(self, surface):
        """Draw stats table"""

        self.render_stats_text(surface, "Maze", 0)
        self.render_stats_text(surface, "Dimensions", 2)
        self.render_stats_text(surface, f"{self.width} x {self.height}", 3)
        self.render_stats_text(surface, "Walls", 5)
        self.render_stats_text(surface, f"{self.walls}", 6)
        self.render_stats_text(surface, "Unvisited", 8)
        self.render_stats_text(surface, f"{self.unvisited}", 9)
        self.render_stats_text(surface, "Visited", 11)
        self.render_stats_text(surface, f"{self.visited}", 12)
        self.render_stats_text(surface, "2nd Vis.", 14)
        self.render_stats_text(surface, f"{self.visited2}", 15)
        self.render_stats_text(surface, "Bumps", 17)
        self.render_stats_text(surface, f"{self.bumps}", 18)

    def generate(self, deep=True, loop_prob=0.05):
        """Generate"""

        x, y = self.x, self.y
        self.loop_prob = loop_prob
        ends = self.walled_neigbour_blocks((x, y))
        while ends:
            if deep:
                x, y = ends.pop()
            else:
                x, y = ends.pop(randrange(len(ends)))
            if self.block_removeable((x, y)):
                self.maze[x][y] = 0
                self.walls -= 1
                self.unvisited += 1
                ends += self.walled_neigbour_blocks((x, y))

    def block_free(self, coord):
        """Block free"""

        x, y = coord[0], coord[1]
        return self.maze[x][y] != -1

    def in_bounds(self, coord):
        """In bounds"""

        x, y = coord[0], coord[1]
        return 0 <= x < self.width and 0 <= y < self.height

    def block_removeable(self, coord):
        """Block removable"""

        if self.block_free(coord):
            return False

        x, y = coord[0], coord[1]
        bl = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        n = 0
        for i in bl:
            if self.in_bounds(i) and self.block_free(i):
                n += 1
        return n <= 1 or random() < self.loop_prob

    def walled_neigbour_blocks(self, coord):
        """Walled neighbour blocks"""

        x, y = coord[0], coord[1]
        bl = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        shuffle(bl)
        rbl = []
        for i in bl:
            if self.in_bounds(i) and not self.block_free(i):
                rbl.append(i)
        return rbl

    def turn(self, n=1):
        """Turn"""

        self.direction += n
        self.direction %= 4

    def move(self):
        """Move"""

        x, y = self.x, self.y
        nx = x + self.dirToDelta[self.direction][0]
        ny = y + self.dirToDelta[self.direction][1]

        if self.in_bounds((nx, ny)) and self.block_free((nx, ny)):
            if self.maze[nx][ny] == 0:
                self.maze[nx][ny] = 1
                self.visited += 1
                self.unvisited -= 1
            elif self.maze[nx][ny] == 1:
                self.maze[nx][ny] = 2
                self.visited2 += 1
            self.x, self.y = nx, ny
            self.moves += 1
        else:
            self.bumps += 1
