"""Reboot"""

import os

import pygame


def load(manager, params):
    """Load"""

    pygame.quit()
    os.system("/sbin/reboot -f")
