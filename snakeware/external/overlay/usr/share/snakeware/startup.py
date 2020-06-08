class Command:
    """Defines a command which is run when repr(self) is evaluated."""

    def run(self):
        raise NotImplementedError

    def __repr__(self):
        """Execute the command."""
        return self.run()


class SnakeWMCommand(Command):
    def run(self):
        """Start SnakeWM."""
        from snakewm.wm import SnakeWM

        return SnakeWM().run()


snakewm = SnakeWMCommand()
