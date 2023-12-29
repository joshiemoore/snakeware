"""
Background picker menu for SnakeBG

Joshua Moore 2020
"""

import os

from pygame import Rect
from pygame_gui.elements import UIButton, UIWindow


class SnakeBGMenu(UIWindow):
    # size of each menu button
    BSIZE = (200, 20)

    def __init__(self, manager):
        # load bg module names
        bgdir = os.path.dirname(os.path.abspath(__file__)) + "/backgrounds/"
        self.BGLIST = []
        for f in os.listdir(bgdir):
            if "__" in f or ".pyc" in f:
                continue
            self.BGLIST.append(f.split(".")[0])
        self.BGLIST = sorted(self.BGLIST)

        # create window
        super().__init__(
            Rect(
                (100, 100), (self.BSIZE[0] + 32, self.BSIZE[1] * len(self.BGLIST))
            ),
            manager=manager,
            window_display_title="SnakeBG",
            object_id="#bgmenu",
            resizable=False,
        )

        # add buttons
        for i in range(len(self.BGLIST)):
            UIButton(
                relative_rect=Rect((0, self.BSIZE[1] * i), self.BSIZE),
                text=self.BGLIST[i],
                manager=manager,
                container=self,
                parent_element=self,
                object_id=self.BGLIST[i],
            )
