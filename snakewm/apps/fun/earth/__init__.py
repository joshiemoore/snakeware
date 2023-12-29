"""Earth"""

from .earth import Earth


def load(manager, params):
    """Create and launch a new instance of Earth."""

    # default position
    pos = (100, 100)

    if params is not None and len(params) > 0:
        pos = params[0]

    Earth(pos, manager)
