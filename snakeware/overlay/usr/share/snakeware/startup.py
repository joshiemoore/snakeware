import os
import readline
import subprocess
from shutil import which
from suplemon.main import App

THE_CODE_FILE = "/tmp/code.py"
# Create an empty file to make sure that `list` and `run` do not crash.
if not os.path.isfile(THE_CODE_FILE):
    with open(THE_CODE_FILE, "w") as fp:
        fp.write("")
THIS_PYTHON = "/usr/bin/python3"
LESS_PRG = which("less")

OUR_SUPLEMON_CONFIG = r"""{
    // Global settings
    "app": {
        "debug": true,
        "debug_level": 20,
        "escdelay": 50,
        "use_unicode_symbols": false,
        "imitate_256color": false
    },
    // Editor settings
    "editor": {
        "auto_indent_newline": true,
        "end_of_line": "\n",
        "backspace_unindent": true,
        "cursor_style": "reverse",
        "default_encoding": "utf-8",
        "hard_tabs": 0,
        "tab_width": 4,
        "max_history": 50,
        "punctuation": " (){}[]<>$@!%'\"=+-/*.:,;_\n\r",
        "line_end_char": "",
        "white_space_map": {
            "\u0000": "\u2400",
            " ": "\u00B7",
            "\t": "\u21B9",
            "\u00A0": "\u237D",
            "\u00AD": "\u2423",
            "\u00A0": "\u2420",
            "\u180E": "\u2420",
            "\u2000": "\u2420",
            "\u2001": "\u2420",
            "\u2002": "\u2420",
            "\u2003": "\u2420",
            "\u2004": "\u2420",
            "\u2005": "\u2420",
            "\u2006": "\u2420",
            "\u2007": "\u2420",
            "\u2008": "\u2420",
            "\u2009": "\u2420",
            "\u200A": "\u2420",
            "\u200B": "\u2420",
            "\u202F": "\u2420",
            "\u205F": "\u2420",
            "\u3000": "\u2420",
            "\uFEFF": "\u2420"
        },
        "show_white_space": false,
        "show_tab_indicators": true,
        "tab_indicator_character": "\u203A",
        "highlight_current_line": true,
        "show_line_nums": true,
        "line_nums_pad_space": true,
        "show_line_colors": true,
        "show_highlighting": true,
        "theme": "monokai",
        "use_mouse": false,
        "use_global_buffer": true,
        "regex_find": false
    },
    // UI Display Settings
    "display": {
        "show_top_bar": true,
        "show_app_name": true,
        "show_file_list": true,
        "show_file_modified_indicator": true,
        "show_legend": true,
        "show_bottom_bar": true,
        "invert_status_bars": false
    }
}
"""
SUPLEMON_CONFIG_FILE = "/tmp/suplemon-config.json"
if not os.path.isfile(SUPLEMON_CONFIG_FILE):
    with open(SUPLEMON_CONFIG_FILE, "w") as fp:
        fp.write(OUR_SUPLEMON_CONFIG)

LIST_OF_COMMANDS = ("edit", "run", "show", "save", "new", "snakewm")


readline.clear_history()


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

    def run(self):
        app = App(filenames=[THE_CODE_FILE], config_file=SUPLEMON_CONFIG_FILE)
        if app.init():
            app.run()
            return "I stored your code."


class RunCommand(Command):
    """Run the only program that we have in THE_CODE_FILE."""

    def run(self):
        _ = subprocess.run([THIS_PYTHON, THE_CODE_FILE])
        return ""


class ListCommand(Command):
    """Use less to show the contents of the only program that we have in 
    THE_CODE_FILE."""

    def run(self):
        _ = subprocess.run([LESS_PRG, THE_CODE_FILE])
        return ""


class NewCommand(Command):
    """Empty the current program"""

    def run(self):
        readline.clear_history()
        with open(THE_CODE_FILE, "w") as fp:
            fp.write("")
        return ""


class SaveCommand(Command):
    """Save the previously entered statements as current program."""

    def run(self):
        previous_cmd_len = readline.get_current_history_length()

        with open(THE_CODE_FILE, "w") as fp:
            for idx in range(1, previous_cmd_len):
                line = readline.get_history_item(idx)
                if line and not line in LIST_OF_COMMANDS:
                    fp.write(readline.get_history_item(idx) + "\n")
        return ""


class SnakeGamesCommand(Command):
    def run(self):
        """Start SnakeWM."""
        from snake_games.gamemenu  import SnakeGameMenu

        return SnakeGameMenu().menu()


snakewm = SnakeWMCommand()

edit = EditCommand()
run = RunCommand()
show = ListCommand()
save = SaveCommand()
new = NewCommand()
snakegames = SnakeGamesCommand()