import os
from pygame import mixer


class Mixer(object):

    # init pygame mixer
    def __init__(self):
        mixer.init()

    # load selected music
    @classmethod
    def load(cls, file):
        mixer.music.load(file)

    # play music
    @classmethod
    def play(cls):
        mixer.music.play()

    # pause music
    @classmethod
    def pause(cls):
        cls.isPaused = True
        mixer.music.pause()

    # resume music
    @classmethod
    def resume(cls):
        mixer.music.unpause()

    # rewind music
    @classmethod
    def rewind(cls):
        mixer.music.rewind()

    # stop music
    @classmethod
    def stop(cls):
        mixer.music.stop()

    # change volume - 0.0 to 1.0
    @classmethod
    def set_volume(cls, value):
        mixer.music.set_volume(value)

    # show the music volume
    @classmethod
    def get_volume(cls):
        return float(mixer.music.get_volume())
