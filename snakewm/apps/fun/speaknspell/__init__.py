"""Speak 'n spell"""

from .speak import SpeakSpell


def load(manager, params):
    """Create and launch a new instance of SpeakSpell."""

    # default position
    pos = (100, 100)

    if params is not None and len(params) > 0:
        pos = params[0]

    SpeakSpell(pos, manager)
