import pygame as pg
import time
pg.init()


class Board:
    matrix = [
        [1, 0, 0, 0, 4, 0, 0, 0, 0],
        [0, 9, 2, 6, 0, 0, 3, 0, 0],
        [3, 0, 0, 0, 0, 5, 1, 0, 0],
        [0, 7, 0, 1, 0, 0, 0, 0, 4],
        [0, 0, 4, 0, 5, 0, 6, 0, 0],
        [2, 0, 0, 0, 0, 4, 0, 8, 0],
        [0, 0, 9, 4, 0, 0, 0, 0, 1],
        [0, 0, 8, 0, 0, 6, 5, 2, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 6]
    ]
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    FPS = 30
    clock = pg.time.Clock()
    # Window Variables
    display_width = 500
    display_height = 500
    display = pg.display.set_mode(
        (display_width, display_height))

    def __init__(self):
        pg.display.set_caption('Sudoku')
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            Board.display.fill(Board.white)
            self.lines()
            self.print_numbers()
            Board.clock.tick(Board.FPS)
            pg.display.update()

    def draw_line(self, color, x, y, width, height):
        #surface, color, (x, y, width, height)
        self.line_x = x
        self.line_y = y
        self.line_width = width
        self.line_height = height
        line = pg.draw.rect(self.display, color, (self.line_x,
                                                  self.line_y, self.line_width, self.line_height))

    def lines(self):
        self.line_distance = int(self.display_height/9)
        self.distance_covered = 0
        self.line_no = 9
        self.thick = 1

        for i in range(self.line_no):
            # Vertical
            if i == 3 or i == 6:
                self.thick = 5
            else:
                self.thick = 1
            self.draw_line(Board.black, self.distance_covered, 0,
                           self.thick, self.display_height)
            # Horizontal
            self.draw_line(Board.black, 0, self.distance_covered,
                           self.display_width, self.thick)
            self.distance_covered += self.line_distance

    def print_stuff(self, font_size, text, color, x, y):
        self.font = pg.font.Font(None, font_size)
        self.text_render = self.font.render(text, 1, color)
        Board.display.blit(self.text_render, (x, y))

    def print_numbers(self):
        gap_horizontal = Board.display_height/9
        gap_vertical = Board.display_height/9

        for i in range(9):
            for j in range(9):
                n = Board.matrix[i][j]
                xx = gap_horizontal*i + 0.3*gap_horizontal
                yy = gap_vertical*j + 0.3*gap_vertical
                if n != 0:
                    self.print_stuff(50, str(n), Board.black, xx, yy)


thing = Board()
thing()
