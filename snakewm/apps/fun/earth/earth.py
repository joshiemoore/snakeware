#!/usr/bin/env python

"""
Draw the day/night distribution in rectangular projection.
Based on renderplanet.py from RSS-Planet (2007-07-17)

Based on Sun position Python code
by Grzegorz Rakoczy
which in turn is based on the web page
 http://www.stjarnhimlen.se/comp/tutorial.html
by Paul Schlyter
"""

from math import *
import os, sys, time

import pygame
import pygame_gui
from pygame_gui.elements.ui_image import UIImage

path = os.path.dirname(os.path.abspath(__file__))

day = path + "/d.jpg"  # images for day
night = path + "/n.jpg"  #   and night

blur = 4.0  # blur angle for terminator

phong = True  # enable Phong shading
shad_div = 260.0  # * shading intensity dividend
#    (higher value -> brighter shading)
diff_int = 1.0  # * diffuse intensity
spec_exp = 4  # * specular reflection exponent
#    (0 = diffuse only; > 50 = metallic)

tpi = 2 * pi
degs = 180 / pi
rads = pi / 180
DIMS = 300, 150  # image size
UPDATE = 600  # update every ten minutes


def init():
    t = time.gmtime(time.time())
    y = t[0]
    m = t[1]
    d = t[2]
    h = t[3]
    mins = t[4]

    h = h + mins / 60.0
    return y, m, d, h


#   Get the days to J2000
#   h is UT in decimal hours
#   FNday only works between 1901 to 2099 - see Meeus chapter 7
def FNday(y, m, d, h):
    days = 367 * y - 7 * (y + (m + 9) // 12) // 4 + 275 * m // 9 + d - 730530 + h / 24.0
    return float(days)


def rev(x):
    rv = x - int(x / 360) * 360
    if rv < 0:
        rv += 360
    return rv


def calc_ra_dec(y, m, d, h):
    global L

    d = FNday(y, m, d, h)

    w = 282.9404 + 4.70935e-5 * d
    a = 1.000000
    e = 0.016709 - 1.151e-9 * d
    M = 356.0470 + 0.9856002585 * d
    M = rev(M)

    oblecl = 23.4393 - 3.563e-7 * d
    L = rev(w + M)

    E = M + degs * e * sin(M * rads) * (1 + e * cos(M * rads))

    x = cos(E * rads) - e
    y = sin(E * rads) * sqrt(1 - e * e)
    r = sqrt(x * x + y * y)
    v = atan2(y, x) * degs
    lon = rev(v + w)

    xequat = r * cos(lon * rads)
    yequat = r * sin(lon * rads) * cos(oblecl * rads)
    zequat = r * sin(lon * rads) * sin(oblecl * rads)

    RA = atan2(yequat, xequat) * degs / 15
    Decl = asin(zequat / r) * degs

    return RA, Decl


def calc_alt(RA, Decl, lat, long, h):
    GMST0 = (L * rads + 180 * rads) / 15 * degs
    SIDTIME = GMST0 + h + long / 15
    HA = rev((SIDTIME - RA)) * 15

    x = cos(HA * rads) * cos(Decl * rads)
    y = sin(HA * rads) * cos(Decl * rads)
    z = sin(Decl * rads)

    xhor = x * sin(lat * rads) - z * cos(lat * rads)
    yhor = y
    zhor = x * cos(lat * rads) + z * sin(lat * rads)

    # azimuth = atan2(yhor, xhor)*degs + 180
    altitude = atan2(zhor, sqrt(xhor * xhor + yhor * yhor)) * degs

    return altitude


def xy2ll(x, y, res):
    lat = 90.0 - float(y) / res[1] * 180.0
    lon = float(x) / res[0] * 360.0 - 180.0
    return lat, lon


def mixp(a, b, x):
    c = []
    for ai, bi in zip(a, b):
        c.append(int((1 - x) * ai + x * bi))
    return tuple(c)


def mul_tup(a, x):
    b = []
    for i in a:
        b.append(int(x * i))
    return tuple(b)


def plot(x, y, alt, width):
    ix = 3 * int(y * width + x)
    if alt > blur and not phong:
        odat[ix : ix + 3] = ddat[ix : ix + 3]
    elif alt > blur:
        dc = ddat[ix : ix + 3]
        nc = ndat[ix : ix + 3]
        i = sin(rads * alt)
        shad_int = min(2.0, max(1.0, shad_div / float(100.0 + dc[0] + dc[1] + dc[2])))
        shad_int *= (shad_int - 0.98) ** 0.2  # reduce brightness in deserts
        odat[ix : ix + 3] = mul_tup(
            dc, 1.0 + 0.5 * (diff_int * i + i**spec_exp) * shad_int
        )
    elif alt < -blur:
        odat[ix : ix + 3] = ndat[ix : ix + 3]
    else:
        dc = ddat[ix : ix + 3]
        nc = ndat[ix : ix + 3]
        odat[ix : ix + 3] = mixp(nc, dc, (alt + blur) / blur / 2.0)


def calc_image(res=DIMS):
    global ddd, nnn, ddat, ndat, odat

    assert res[1] % 2 == 0, "Odd vertical resolutions not supported."

    ddd = pygame.image.load(day)
    nnn = pygame.image.load(night)

    ddat = pygame.image.tostring(ddd, "RGB")
    ndat = pygame.image.tostring(nnn, "RGB")
    odat = 3 * res[0] * res[1] * []

    y, m, d, h = init()
    ra, dec = calc_ra_dec(y, m, d, h)
    hx = res[0] / 2
    hy = res[1] / 2

    for y in range(int(res[1])):
        for x in range(res[0]):
            lat, lon = xy2ll(x, y, res)
            alt = calc_alt(ra, dec, lat, lon, h)
            plot(x, y, alt, res[0])
    for n in range(len(odat)):
        odat[n] = max(0, min(255, odat[n]))

    output = bytes(odat)
    result = pygame.image.fromstring(output, res, "RGB")
    return result


class Earth(pygame_gui.elements.UIWindow):
    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (DIMS[0] + 32, DIMS[1] + 60)),
            manager=manager,
            window_display_title="earth",
            object_id="#earth",
        )

        self.dsurf = UIImage(
            pygame.Rect((0, 0), DIMS),
            pygame.Surface(DIMS).convert(),
            manager=manager,
            container=self,
            parent_element=self,
        )
        self.last = 0
        self.start = True

    def process_event(self, event):
        super().process_event(event)

    def update(self, delta):
        super().update(delta)
        if self.start:
            self.start = False
            super().set_display_title("rendering image, please wait")
            return
        else:
            super().set_display_title("earth")
        if time.time() - self.last > UPDATE:
            self.last = time.time()
            self.out = calc_image()
        self.dsurf.image.blit(self.out, (0, 0))
