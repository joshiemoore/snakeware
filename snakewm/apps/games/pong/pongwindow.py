import pygame
import pygame_gui

from pygame_gui.elements.ui_image import UIImage
from pygame_gui.elements.ui_window import UIWindow

from .pong import PongGame


class PongWindow(UIWindow):
    def __init__(self, position, ui_manager):
        super().__init__(
            pygame.Rect(position, (320, 240)),
            ui_manager,
            window_display_title="pong",
            object_id="#pong_window",
        )

        game_surface_size = self.get_container().get_size()
        self.game_surface_element = UIImage(
            pygame.Rect((0, 0), game_surface_size),
            pygame.Surface(game_surface_size).convert(),
            manager=ui_manager,
            container=self,
            parent_element=self,
        )

        self.pong_game = PongGame(game_surface_size)

        self.is_active = False

    def focus(self):
        self.is_active = True

    def unfocus(self):
        self.is_active = False

    def process_event(self, event):
        handled = super().process_event(event)
        if (
            event.type == pygame.USEREVENT
            and event.user_type == pygame_gui.UI_BUTTON_PRESSED
            and event.ui_object_id == "#pong_window.#title_bar"
            and event.ui_element == self.title_bar
        ):
            handled = True
            event_data = {
                "user_type": "window_selected",
                "ui_element": self,
                "ui_object_id": self.most_specific_combined_id,
            }
            window_selected_event = pygame.event.Event(pygame.USEREVENT, event_data)
            pygame.event.post(window_selected_event)
        if self.is_active:
            handled = self.pong_game.process_event(event)
        return handled

    def update(self, time_delta):
        if self.alive() and self.is_active:
            self.pong_game.update(time_delta)

        super().update(time_delta)

        self.pong_game.draw(self.game_surface_element.image)
