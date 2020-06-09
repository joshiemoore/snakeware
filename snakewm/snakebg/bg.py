"""
SnakeBG - dynamic backgrounds for SnakeWM!

Joshua Moore 2020
"""

import importlib


class SnakeBG:
    # reference to the imported background
    _BG = None

    def __init__(self, bgname, testmode):
        bgmod = "snakebg.backgrounds." + bgname
        if not testmode:
            bgmod = "snakewm." + bgmod

        # actually import the background
        self._BG = importlib.import_module(bgmod)

    def draw(self, surface):
        # draw the background if the _BG module is set
        if self._BG is None:
            return

        self._BG.drawbg(surface)
