class Win:
    def __repr__(self):
        from snakewm.wm import SnakeWM
        return SnakeWM().run()


win = Win()
