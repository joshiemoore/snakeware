"""Snake paint"""

from .snakepaint import SnakePaint


def load():
    """Load"""

    app = SnakePaint()
    app.on_execute()
    del app
