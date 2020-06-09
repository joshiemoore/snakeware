"""
Fading color background for SnakeBG

Joshua Moore 2020
"""

FCOLOR_R = 0
FCOLOR_G = 0
FCOLOR_B = 0
FCOLOR_STEP = 1


def drawbg(surface):
    global FCOLOR_R
    global FCOLOR_G
    global FCOLOR_B
    global FCOLOR_STEP

    surface.fill((FCOLOR_R, FCOLOR_G, FCOLOR_B))

    if FCOLOR_STEP > 0:
        if FCOLOR_R < 255:
            FCOLOR_R = FCOLOR_R + FCOLOR_STEP
        elif FCOLOR_G < 255:
            FCOLOR_G = FCOLOR_G + FCOLOR_STEP
        elif FCOLOR_B < 255:
            FCOLOR_B = FCOLOR_B + FCOLOR_STEP
        else:
            FCOLOR_STEP = -FCOLOR_STEP
    elif FCOLOR_STEP < 0:
        if FCOLOR_R > 0:
            FCOLOR_R = FCOLOR_R + FCOLOR_STEP
        elif FCOLOR_G > 0:
            FCOLOR_G = FCOLOR_G + FCOLOR_STEP
        elif FCOLOR_B > 0:
            FCOLOR_B = FCOLOR_B + FCOLOR_STEP
        else:
            FCOLOR_STEP = -FCOLOR_STEP
