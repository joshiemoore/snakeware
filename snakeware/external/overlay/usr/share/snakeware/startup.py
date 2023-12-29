"""Startup"""


class Command:
    """Defines a command which is run when repr(self) is evaluated."""

    def run(self) -> None:
        """Run"""

        raise NotImplementedError

    def __repr__(self) -> None:
        """Execute the command."""

        return self.run()


class SnakeWMCommand(Command):
    """SnakeWM command"""

    def run(self) -> None:
        """Start SnakeWM."""

        from snakewm.wm import SnakeWM

        return SnakeWM().run()


class ShutdownCommand(Command):
    """Shutdown command"""

    def run(self) -> None:
        """Run"""

        import os

        os.system("/sbin/poweroff -f")


class RebootCommand(Command):
    """Reboot command"""

    def run(self) -> None:
        """Run"""

        import os

        os.system("/sbin/reboot -f")


snakewm = SnakeWMCommand()
shutdown = ShutdownCommand()
reboot = RebootCommand()
