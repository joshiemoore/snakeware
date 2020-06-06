from .snakepaint import SnakePaint


def load():
    app = SnakePaint()
    app.on_execute()
    del app
