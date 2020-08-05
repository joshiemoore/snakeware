import pygame
import os
from math import cos, sin, tan, pi, floor, ceil, sqrt

two_pi = pi * 2
half_pi = pi * 0.5 
three_half_pi = pi * 1.5

NUMBER_OF_RAYS = 320

class Maze3D:
    def __init__(self, size):

        app_path = os.path.dirname(os.path.abspath(__file__))
        assets_path = app_path + "/assets"

        self.size = size
        self.width = self.size[0]
        self.height = self.size[1]
        

        # Load the wall texture images
        # ALL THE IMAGES SHOULD HAVE THE SAME SIZE.
        self.walldark = [None]
        self.walllight = [None]
        
        self.walldark.append(pygame.image.load(assets_path + "/wall2_dark.png").convert())
        self.walllight.append(pygame.image.load(assets_path + "/wall2_light.png").convert())

        self.walldark.append(pygame.image.load(assets_path + "/wall3_dark.png").convert())
        self.walllight.append(pygame.image.load(assets_path + "/wall3_light.png").convert())

        self.textureSize = self.walldark[1].get_size()
        
        # Background image
        self.bg_img = pygame.image.load(assets_path + "/maze_bg.png").convert()
        self.bg_img = pygame.transform.scale(self.bg_img, size)
        
        # Initialize vars and create the map
        self.playerX = 1.5
        self.playerY = 1.5
        self.playerDir = 0.0
        
        self.playerStep = 0.05
        self.angleStep = 5.0 * pi / 180.0

        self.toggleTurnLeft = False
        self.toggleTurnRight = False
        self.toggleMoveFw = False
        self.toggleMoveBw = False

        self.defaultHeight = 400.0

        self.numRays = NUMBER_OF_RAYS
        self.viewAngle = 65 * pi / 180.0 # 105 degrees in radians

        self.rayAngleStep = self.viewAngle / (self.numRays - 1)
        self.columnWidth = self.width / (self.numRays-1)

        self.map = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,1],
            [1,0,1,0,1,1,1,0,1,0,1,1,0,1,0,1,1,0,1,0,1,1,1,0,1,0,1,0,0,1,0,1],
            [1,1,1,0,1,0,0,0,1,0,1,0,0,0,0,1,1,0,1,0,0,1,0,0,1,0,0,0,1,0,1,1],
            [1,0,0,0,0,0,1,1,1,0,1,0,1,1,1,1,0,0,0,1,0,1,0,1,1,1,1,0,1,0,1,1],
            [1,0,1,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1],
            [1,0,1,0,1,0,1,1,0,1,0,0,0,1,0,1,0,0,0,1,1,1,0,0,0,1,0,1,1,1,0,1],
            [1,1,1,0,1,0,0,1,0,1,1,1,1,1,0,1,1,0,1,0,0,1,1,1,1,1,0,1,0,1,1,1],
            [1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,1,0,1,0,1,0,0,0,0,1,0,0,0,0,0,1],
            [1,1,1,1,0,1,1,1,1,0,0,1,0,1,1,1,1,0,0,0,0,0,1,1,0,1,1,1,1,1,0,1],
            [1,0,0,1,0,1,0,1,0,1,1,0,0,1,0,0,0,1,1,1,1,0,0,1,0,0,1,0,0,0,0,1],
            [1,1,0,1,0,1,0,0,0,1,0,0,1,0,0,1,0,0,0,1,1,1,1,1,1,1,1,0,1,1,1,1],
            [1,0,0,0,0,1,0,1,0,0,0,1,0,1,1,1,1,1,0,1,0,0,0,0,0,0,1,0,0,0,1,1],
            [1,1,0,1,1,0,1,1,0,1,1,1,0,1,0,0,0,0,0,0,0,1,1,1,1,0,0,1,1,0,0,1],
            [1,0,0,1,1,0,0,0,0,1,0,0,0,0,0,1,0,1,1,1,0,1,0,0,1,1,0,1,0,1,0,1],
            [1,0,1,1,0,0,1,1,1,0,0,1,1,0,1,1,0,0,0,1,1,1,0,0,0,1,0,1,0,0,0,1],
            [1,1,1,0,0,1,0,0,0,1,0,0,1,0,1,0,0,1,0,0,0,0,0,1,0,1,0,0,1,0,1,1],
            [1,0,0,0,1,1,1,1,0,0,0,1,0,0,1,0,1,1,0,1,1,1,0,1,0,1,1,0,1,0,0,1],
            [1,0,1,0,0,0,0,0,1,1,1,1,1,0,1,1,1,0,0,1,0,0,1,1,0,1,1,0,1,1,0,1],
            [1,0,0,1,1,1,1,0,0,1,0,0,0,0,0,1,0,0,1,2,1,0,0,0,0,1,0,0,1,0,0,1],
            [1,1,0,0,1,0,0,1,0,1,0,1,1,1,0,1,0,1,1,0,1,0,1,0,1,1,0,1,1,1,0,1],
            [1,0,0,1,1,0,1,1,0,0,1,1,0,0,0,0,1,1,1,0,0,0,1,0,1,0,0,1,0,0,0,1],
            [1,0,1,1,0,0,0,1,1,0,1,0,0,1,1,0,0,0,1,1,1,1,0,1,1,0,1,0,0,1,1,1],
            [1,0,1,0,0,1,0,0,1,0,0,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,0,1,1,0,1],
            [1,0,1,0,1,1,1,0,1,1,0,1,1,0,1,0,0,1,1,0,1,1,1,1,1,1,1,0,0,0,0,1],
            [1,0,1,0,1,0,0,0,1,0,0,1,1,0,1,1,0,0,1,0,0,1,0,0,0,0,1,1,1,0,1,1],
            [1,0,1,0,1,1,1,1,1,1,0,1,0,0,1,0,1,0,0,1,0,0,0,1,1,0,1,0,0,0,0,1],
            [1,0,1,0,0,0,1,1,0,0,0,1,0,1,1,0,1,1,0,1,1,1,1,0,1,0,1,0,1,0,1,1],
            [1,0,1,1,1,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1],
            [1,0,0,0,1,1,0,1,1,1,0,1,1,0,0,0,1,1,0,1,1,0,1,0,0,1,1,1,0,1,0,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]

    # Update player position according to flags set by process_event
    # Called each frame to get smooth movement
    def updatePos(self) :
        if self.toggleTurnLeft :
            self.playerDir = (self.playerDir + self.angleStep) % (two_pi)
        if self.toggleTurnRight :
            self.playerDir = (self.playerDir - self.angleStep) % (two_pi)
        if self.toggleMoveFw :
            self.move(1)
        if self.toggleMoveBw :
            self.move(-1)


    # Move forward or backward
    def move(self, dir):
        flag = False
        x, y = self.playerX, self.playerY
        # Calculating new coords
        nx = x + self.playerStep * dir * cos(self.playerDir)
        ny = y - self.playerStep * dir * sin(self.playerDir)
        # Case : no obstacle
        if self.map[floor(ny)][floor(nx)] == 0 :
            self.playerX, self.playerY = nx, ny
            return
        # Case : wall placed orthogonally
        if floor(x) == floor(nx) and floor(y) == floor(ny)+1 :
            self.playerX, self.playerY = nx, ceil(ny)+0.01
            return
        if floor(x) == floor(nx) and floor(y) == floor(ny)-1 :
            self.playerX, self.playerY = nx, floor(ny)-0.01
            return
        if floor(x) == floor(nx)+1 and floor(y) == floor(ny) :
            self.playerX, self.playerY = ceil(nx)+0.01, ny
            return
        if floor(x) == floor(nx)-1 and floor(y) == floor(ny) :
            self.playerX, self.playerY = floor(nx)-0.01, ny
            return
        # Special case where we hit a corner
        if self.map[floor(ny)][floor(x)] == 0 and self.map[floor(y)][floor(nx)] == 0 :
            flag = True
        # Handle cases where we cross wall separation and hit diagonally
        self.playerX, self.playerY = nx, ny
        if floor(x) == floor(nx)+1 and floor(y) == floor(ny)+1 : # 1
            if self.map[floor(ny)][floor(x)] != 0 or flag :
                self.playerY = ceil(ny)+0.01
            if self.map[floor(y)][floor(nx)] != 0 or flag :
                self.playerX = ceil(nx)+0.01
            return
        if floor(x) == floor(nx)-1 and floor(y) == floor(ny)+1 : # 2
            if self.map[floor(ny)][floor(x)] != 0 or flag :
                self.playerY = ceil(ny)+0.01
            if self.map[floor(y)][floor(nx)] != 0 or flag :
                self.playerX = floor(nx)-0.01
            return
        if floor(x) == floor(nx)-1 and floor(y) == floor(ny)-1 : # 3
            if self.map[floor(ny)][floor(x)] != 0 or flag :
                self.playerY = floor(ny)-0.01
            if self.map[floor(y)][floor(nx)] != 0 or flag :
                self.playerX = floor(nx)-0.01
            return
        if floor(x) == floor(nx)+1 and floor(y) == floor(ny)-1 : # 4
            if self.map[floor(ny)][floor(x)] != 0 or flag :
                self.playerY = floor(ny)-0.01
            if self.map[floor(y)][floor(nx)] != 0 or flag :
                self.playerX = ceil(nx)+0.01
            return

    # Key handling set flags for updatePos
    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.toggleTurnLeft = True
            elif event.key == pygame.K_RIGHT:
                self.toggleTurnRight = True
            elif event.key == pygame.K_UP:
                self.toggleMoveFw = True
            elif event.key == pygame.K_DOWN:
                self.toggleMoveBw = True
            else:
                return False
            return True
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_LEFT:
                self.toggleTurnLeft = False
            elif event.key == pygame.K_RIGHT:
                self.toggleTurnRight = False
            elif event.key == pygame.K_UP:
                self.toggleMoveFw = False
            elif event.key == pygame.K_DOWN:
                self.toggleMoveBw = False
            else:
                return False
            return True
        return False

    # Raycaster written thanks to https://www.playfuljs.com/a-first-person-engine-in-265-lines/
    # and https://youtu.be/gYRrGTC7GtA
    def draw(self, surface):
        # set background image
        surface.blit(self.bg_img, (0, 0))
        for r in range(self.numRays) :
            # ray angle with the horizontal
            rayAngle = (self.playerDir + (self.viewAngle / 2) - r * self.rayAngleStep) % (two_pi)
            # check distance with vertical lines (ray goes to the left or right, hence the variables name)
            distH = 100000 # default distance
            propH = 0 # to know what part of the texture to draw
            if rayAngle != half_pi and rayAngle != three_half_pi :
                tanRayAngle = tan(rayAngle)
                if rayAngle < half_pi or rayAngle > three_half_pi : # ray goes to the right
                    x = ceil(self.playerX)
                    y = self.playerY - tanRayAngle * (x - self.playerX)
                    dir = 1
                else :  # ray goes to the left
                    x = floor(self.playerX)
                    y = self.playerY - tanRayAngle * (x - self.playerX)
                    dir = -1
                while y > 0 and y < len(self.map) and self.map[floor(y)][floor(x+0.1*dir)] == 0 : # going from column to column
                    x += dir
                    y -= dir*tanRayAngle
                if y > 0 and y < len(self.map) : # we found a wall
                    wallTypeH = self.map[floor(y)][floor(x+0.1*dir)]
                    distH = sqrt((self.playerX-x)*(self.playerX-x) + (self.playerY-y)*(self.playerY-y))
                    propH = y%1 if dir == 1 else 1-(y%1)

            # check distance with horizontal lines
            distV = 100000
            propV = 0
            if rayAngle != 0 and rayAngle != pi :
                arctanRayAngle = 1.0 / tan(rayAngle)
                if rayAngle < pi : # ray goes up
                    y = floor(self.playerY)
                    x = self.playerX + arctanRayAngle * (self.playerY - y)
                    dir = -1
                else : # ray goes down
                    y = ceil(self.playerY)
                    x = self.playerX + arctanRayAngle * (self.playerY - y)
                    dir = 1
                while x > 0 and x < len(self.map[0]) and self.map[floor(y+0.1*dir)][floor(x)] == 0 : # going from row to row
                    y += dir
                    x -= dir*arctanRayAngle
                if x > 0 and x < len(self.map[0]) :# we found a wall
                    wallTypeV = self.map[floor(y+0.1*dir)][floor(x)]
                    distV = sqrt((self.playerX-x)*(self.playerX-x) + (self.playerY-y)*(self.playerY-y))
                    propV = x%1 if dir == -1 else 1-(x%1)
            # take min distance and prepare texture to be used
            if distH < distV :
                dist = distH
                prop = propH
                wallImg = self.walllight[wallTypeH]
            else :
                coeffLight = 1.0
                dist = distV
                prop = propV
                wallImg = self.walldark[wallTypeV]
            z = max(0.01, dist * cos((rayAngle - self.playerDir))) # correction for fisheye effect
            # draw wall slice
            calculatedHeight = self.defaultHeight*(1 / z)
            if calculatedHeight > self.height :
                h = self.height
                cropHeight = self.height /calculatedHeight * self.textureSize[1] # if we're too close and don't see the wall entirely
                offset = (self.textureSize[1] - cropHeight) / 2
            else : 
                h = calculatedHeight
                cropHeight = self.textureSize[1]
                offset = 0
            cropArea = (self.textureSize[0]*prop, offset, 1, cropHeight)
            croppedImg = wallImg.subsurface(cropArea) # select the part of the texture to be drawn
            sliceShape = (ceil(self.columnWidth), floor(h+0.5))
            wallSliceImg = pygame.transform.scale(croppedImg, sliceShape)
            surface.blit(wallSliceImg, (r * self.columnWidth, (self.height - h)/2))
    
