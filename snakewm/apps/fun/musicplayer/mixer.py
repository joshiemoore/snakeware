"""Mixer"""

from pygame import mixer


class Mixer(object):
    """Mixer"""

    # init pygame mixer
    def __init__(self):
        mixer.init()

    # load selected music
    @classmethod
    def load(cls, file):
        """Load"""

        mixer.music.load(file)

    @classmethod
    def play(cls):
        """Play music"""

        mixer.music.play()

    @classmethod
    def pause(cls):
        """Pause music"""

        cls.isPaused = True
        mixer.music.pause()

    @classmethod
    def resume(cls):
        """Resume music"""

        mixer.music.unpause()

    @classmethod
    def rewind(cls):
        """Rewind music"""

        mixer.music.rewind()

    @classmethod
    def stop(cls):
        """Stop music"""

        mixer.music.stop()

    @classmethod
    def set_volume(cls, value):
        """Change volume - 0.0 to 1.0"""

        mixer.music.set_volume(value)

    @classmethod
    def get_volume(cls):
        """Get the music volume"""

        return float(mixer.music.get_volume())
