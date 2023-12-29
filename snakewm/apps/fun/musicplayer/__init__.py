"""Music player"""

from .musicplayer import MusicPlayer


def load(manager, params):
    """Create and launch a new instance of MusicPlayer."""

    # default position
    pos = (100, 100)

    if params is not None and len(params) > 0:
        pos = params[0]

    MusicPlayer(pos, manager)
