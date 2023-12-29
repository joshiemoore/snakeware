"""Snake"""

from .sgame import SnakeApp


def load():
    """Load"""

    app = SnakeApp()
    app.on_execute()
    del app
