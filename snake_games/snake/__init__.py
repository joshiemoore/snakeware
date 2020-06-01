from .sgame import SnakeApp

def load():
    app = SnakeApp()
    app.on_execute()
    del app
