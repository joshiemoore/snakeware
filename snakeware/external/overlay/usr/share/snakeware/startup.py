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


class ShutdownCommand(Command):
    def run(self):
        import os
        os.system("/sbin/poweroff -f")


class RebootCommand(Command):
    def run(self):
        import os
        os.system("/sbin/reboot -f")


snakewm = SnakeWMCommand()
shutdown = ShutdownCommand()
reboot = RebootCommand()
