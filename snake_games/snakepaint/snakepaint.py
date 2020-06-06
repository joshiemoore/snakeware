import pygame, random, os


def roundline(srf, color, start, end, radius=1):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(srf, color, (x, y), radius)


class SnakePaint:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.draw_on = False
        self.last_pos = (0, 0)
        self.color = (255, 128, 0)
        self.radius = 10

    def on_init(self):
        pygame.init()

        os.putenv("SDL_FBDEV", "/dev/fb0")
        pygame.display.init()

        self.DIMS = (pygame.display.Info().current_w, pygame.display.Info().current_h)

        self._display_surf = pygame.display.set_mode(self.DIMS, pygame.FULLSCREEN)

        self._running = True



    def on_execute(self):
        self.on_init()
        self.start()



    def start(self):
        while self._running:
            keys = pygame.key.get_pressed()
            e = pygame.event.wait()
            if keys[pygame.K_ESCAPE]:
                self._running = False
            pygame.event.pump()
            if e.type == pygame.MOUSEBUTTONDOWN:
                self.color = (random.randrange(256), random.randrange(256), random.randrange(256))
                pygame.draw.circle(self._display_surf, self.color, e.pos, self.radius)
                self.draw_on = True
            if e.type == pygame.MOUSEBUTTONUP:
                self.draw_on = False
            if e.type == pygame.MOUSEMOTION:
                if self.draw_on:
                    pygame.draw.circle(self._display_surf, self.color, e.pos, self.radius)
                    roundline(self._display_surf, self.color, e.pos, self.last_pos, self.radius)
                self.last_pos = e.pos
            pygame.display.flip()


obj = SnakePaint()
obj.on_execute()
