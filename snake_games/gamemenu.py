"""Game menu"""

import importlib
import os


class SnakeGameMenu:
    """Snake Game Menu"""

    GAMENUMS = "0123456789"

    def __init__(self):
        self.GAMEPATH = os.path.dirname(os.path.abspath(__file__))
        self.LIST = []
        self.cur_page = 0

        for file in os.listdir(self.GAMEPATH):
            if os.path.isdir(self.GAMEPATH + "/" + file) and os.path.isfile(
                self.GAMEPATH + "/" + file + "/__init__.py"
            ):
                self.LIST.append(file)

    def list_page(self):
        """List all the games on the current page."""

        page_idx = self.cur_page * 10

        for i in range(10):
            if i + page_idx >= len(self.LIST):
                break
            print("    " + str(i) + ". " + self.LIST[i + page_idx])
        print("")

    def list_games(self):
        """
        Render the full current page for the games list, including the
        header and prompt for user input.
        """

        os.system("clear")

        print("\n\n~~~~~ SNAKE GAMES ~~~~~\n")
        print("  Page {0}/{1}:".format(self.cur_page + 1, int(len(self.LIST) / 10 + 1)))

        self.list_page()

        print("  0-9: Select Game")
        print("  +  : Next Page")
        print("  -  : Prev Page")
        print("  q  : Quit\n")

        resp = input("  >")

        if resp == "q":
            # quit
            exit()
        elif resp == "+":
            # next page
            if self.cur_page < int(len(self.LIST) / 10):
                self.cur_page = self.cur_page + 1
        elif resp == "-":
            # prev page
            if self.cur_page > 0:
                self.cur_page = self.cur_page - 1
        elif len(resp) == 1 and resp in self.GAMENUMS:
            # load selected game
            sidx = self.cur_page * 10 + int(resp)

            if sidx >= len(self.LIST):
                return

            print("Loading " + self.LIST[sidx] + "...")

            game = "snake_games." + self.LIST[sidx]
            _game = importlib.import_module(game)
            _game.load()

            exit()

    def menu(self):
        """Menu"""

        while True:
            self.list_games()
