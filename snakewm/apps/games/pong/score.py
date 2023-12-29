"""Score"""

from pygame import Color


class Score:
    """Score"""

    def __init__(self, font):
        self.player_1_score = 0
        self.player_2_score = 0
        self.font = font

        self.score_string = None
        self.score_text_render = None

        self.update_score_text()

    def update_score_text(self):
        """Update score text"""

        self.score_string = str(self.player_1_score) + " - " + str(self.player_2_score)
        self.score_text_render = self.font.render(
            self.score_string, True, Color(200, 200, 200)
        )

    def render(self, screen, size):
        """Render"""

        screen.blit(
            self.score_text_render,
            self.score_text_render.get_rect(centerx=size[0] / 2, centery=size[1] / 10),
        )

    def increase_player_1_score(self):
        """Increase player 1 score"""

        self.player_1_score += 1
        self.update_score_text()

    def increase_player_2_score(self):
        """Increase player 2 score"""

        self.player_2_score += 1
        self.update_score_text()
