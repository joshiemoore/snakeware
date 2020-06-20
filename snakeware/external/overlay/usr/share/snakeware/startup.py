import os

# mount SNAKEUSER again if the first one didn't catch it.
# If it's already mounted, nothing will happen.
code = os.system("mount -t ext4 /dev/disk/by-label/SNAKEUSER /snakeuser 2>/dev/null")

elif int(code) != 0:
    print("Looks like your persistent partition could not be found. If you did make a persistent partition, try running exit(). If that doesn't work, then something went wrong with your drive or with your partition.")

os.chdir("/snakeuser")


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
        
        os.system("/sbin/poweroff -f")


class RebootCommand(Command):
    def run(self):

        os.system("/sbin/reboot -f")


snakewm = SnakeWMCommand()
shutdown = ShutdownCommand()
reboot = RebootCommand()
