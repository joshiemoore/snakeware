"""Mixer"""

from pygame import mixer


class Mixer(object):
    """Mixer"""

    # init pygame mixer
    def __init__(self):
        mixer.init()

    @staticmethod
    def load(file):
        """Load selected music"""

        mixer.music.load(file)

    @staticmethod
    def play():
        """Play music"""

        mixer.music.play()

    @classmethod
    def pause(cls):
        """Pause music"""

        cls.isPaused = True
        mixer.music.pause()

    @staticmethod
    def resume():
        """Resume music"""

        mixer.music.unpause()

    @staticmethod
    def rewind():
        """Rewind music"""

        mixer.music.rewind()

    @staticmethod
    def stop():
        """Stop music"""

        mixer.music.stop()

    @staticmethod
    def set_volume(value):
        """Change volume - 0.0 to 1.0"""

        mixer.music.set_volume(value)

    @staticmethod
    def get_volume():
        """Get the music volume"""

        return float(mixer.music.get_volume())
