# snake_games

This is the user-made games repository for snakeware. These games come shipped
standard with every snakeware release. We are only going to include fun free
games made by amateurs here.

To run these games, boot into snakeware and enter these commands:

```
>>> import snake_games
>>> snake_games.menu()
```

This will launch an interactive menu where you can select a game to play. Also,
if you already know the name of the game you want, you can import and run it
directly like this:

```
>>> import snake_games.snake
>>> snake_games.snake.load()
```

## Contributing

If you would like to include your game in snake_games, please send a PR adding
it to this directory! However, it's important to note that you will need to
make some changes to your game before it will run in the snakeware environment.
PRs will be approved if they meet the following guidelines:

* Your game must be written in Python.

* Your game must have an `__init__.py` with a `load()` function which creates
an instance of your game and launches it. Please see existing games in this
directory for examples of how this works.

* Your game must be fullscreen, and it must draw directly to the framebuffer.
You can set pygame to fbdev mode by adding `os.putenv('SDL_FBDEV', '/dev/fb0')`
right before your call to `pygame.display.init()`.

* You should not try to set the dimensions of the pygame window, but should
instead get the dimensions of the full-screen display after calling
`pygame.display.init()` like so:

```
DIMS = (
    pygame.display.Info().current_w,
    pygame.display.Info().current_h
)
```
You should write your game so that it handles these varying screen dimensions
gracefully.

* Your game must have a way for the user to immediately exit and return to
snakeware at any time, preferably by pressing the `ESC` key.

* Please test your game before submitting a PR. At minimum, you should try
launching your game as root from a different TTY to verify that your game works
as expected without X Windows running.

Feel free to reach out if you have any questions while you're modifying your
game to run on snakeware!

Also, your game does not have to be based on pygame. We will accept other
libraries as long as they allow you to draw directly to the framebuffer, and
your game meets the above guidelines.

We would be happy to accept text-based/console games as well!
