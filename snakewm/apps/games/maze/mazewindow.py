import pygame
import pygame_gui

from pygame_gui.ui_manager import UIManager
from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.elements.ui_image import UIImage

from .maze import Maze

class MazeWindow(UIWindow):
    def __init__(self, position, ui_manager):
        super().__init__(
            pygame.Rect(position, (640, 480)),
            ui_manager,
            window_display_title="maze",
            object_id="#maze_window",
        )

        game_surface_size = self.get_container().get_size()
        self.game_surface_element = UIImage(
            pygame.Rect((0, 0), game_surface_size),
            pygame.Surface(game_surface_size).convert(),
            manager=ui_manager,
            container=self,
            parent_element=self,
        )

        self.maze = Maze(game_surface_size)

    def process_event(self, event):
        super().process_event(event)
        return self.maze.process_event(event)

    def update(self, time_delta):
        super().update(time_delta)
        self.maze.draw(self.game_surface_element.image)
