class SnakeWMCommand:
    def __repr__(self):
        from snakewm.wm import SnakeWM
        return SnakeWM().run()


snakewm = SnakeWMCommand()
