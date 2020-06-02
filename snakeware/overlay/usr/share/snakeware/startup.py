import subprocess
from shutil import which
from suplemon.main import App


THE_CODE_FILE = "/tmp/code.py"
THIS_PYTHON = "/usr/bin/python3"
LESS_PRG = which("less")


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


class EditCommand(Command):
    """Start suplemon with this single file to edit."""

    def __repr__(self):
        app = App(filenames=[THE_CODE_FILE])
        if app.init():
            app.run()
            return "I stored your code."


class RunCommand:
    """Run the only program that we have in THE_CODE_FILE."""

    def __repr__(self):
        _ = subprocess.run([THIS_PYTHON, THE_CODE_FILE])
        return ""


class ListCommand:
    """Use less to show the contents of the only program that we have in 
    THE_CODE_FILE."""

    def __repr__(self):
        _ = subprocess.run([LESS_PRG, THE_CODE_FILE])
        return ""


snakewm = SnakeWMCommand()

edit = EditCommand()
run = RunCommand()
list = ListCommand()
