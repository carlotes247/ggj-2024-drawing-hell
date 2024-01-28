import os
# import basic pygame modules
import pygame as pg
import math
import numpy as np

main_dir = os.path.split(os.path.abspath(__file__))[0]


class DrawSurface:
    
    def __init__(self, parent, position):
        
        self.rect = position
        
        self.surf = pg.Surface((self.rect.w, self.rect.h), pg.SRCALPHA)
        self.surf.fill([255, 255, 255, 0])
        self.idxArr = np.mgrid[:self.rect.w, : self.rect.h].astype(np.float32)
        
        self.size = 144
        self.color = np.asarray((0, 0, 0))
        
    def getDist(self, pos):
        iArr = self.idxArr.copy()
        iArr[0] -= pos[0]
        iArr[1] -= pos[1]
        
        iArr = np.power(iArr, 2)
        
        return np.sum(iArr, axis = 0 )
    
    def setColor(self, col):
        self.color = np.asarray(col)
    
    def setSize(self, size):
        self.size = size ** 2
   
    def clear(self):
        self.surf.fill([255, 255, 255, 0])
    
    def getResultImage(self):
        pixArr = pg.surfarray.pixels3d(self.surf)
        area = self.idxArr[:, (pixArr[..., 0] < 255) & (pixArr[..., 1] < 255) & (pixArr[..., 2] < 255)]
        if (area.shape[0] == 0 or area.shape[1] == 0):
            sur = pg.Surface((32, 32), pg.SRCALPHA)
            sur.fill([255, 255, 255, 0])
            return sur
        minX, minY = int(np.min(area[0])), int(np.min(area[1]))
        maxX, maxY = int(np.max(area[0])), int(np.max(area[1]))
        msk = ((pixArr[..., 0] < 255) & (pixArr[..., 1] < 255) & (pixArr[..., 2] < 255))[minX : maxX, minY: maxY].copy()
        del pixArr
        
        sur = pg.Surface((maxX - minX, maxY - minY), pg.SRCALPHA)
        sur.fill([255, 255, 255, 0])
        sur.blit(self.surf, (0, 0), (minX, minY, maxX - minX, maxY - minY))
        #write alpha
        aArr = pg.surfarray.pixels_alpha(sur)
        aArr[~msk] = 0
        del aArr
        return sur
    
    def update(self, screen, state):
        mouse_pressed = pg.mouse.get_pressed(num_buttons = 3)
        pos = pg.mouse.get_pos()
        rel = pg.mouse.get_rel()
        self.pixArr = pg.surfarray.pixels3d(self.surf)
        self.aArr = pg.surfarray.pixels_alpha(self.surf)
        
        xFactor = -min(rel[0] / max(rel[1], 1), 1) * math.sqrt(self.size) / 3
        yFactor = -min(rel[1] / max(rel[0], 1), 1) * math.sqrt(self.size) / 3
        
        if (mouse_pressed[2] or mouse_pressed[0]):
            x = pos[0]
            y = pos[1]
            while (rel[0] < 0 and x < (pos[0] - rel[0])) or (rel[0] >= 0 and x > (pos[0] - rel[0])) or (rel[1] < 0 and y < (pos[1] - rel[1])) or (rel[1] >= 0 and y > (pos[1] - rel[1])):
                p = (x, y)
                x += xFactor
                y += yFactor
                if (self.rect.collidepoint(p)):
                    drawPos = (p[0] - self.rect.x, p[1] - self.rect.y)
                    if (mouse_pressed[2]): #right button pressed
                        radius = self.getDist(drawPos)
                        msk = radius < self.size
                        self.pixArr[msk] = [255, 255, 255]
                        self.aArr[msk] = 0
                    elif (mouse_pressed[0]): #leftbutton pressed
                        radius = self.getDist(drawPos)
                        msk = radius < self.size
                        a = ((self.size - radius[msk]) / self.size)
                        
                        t = 255
                        t = np.minimum(self.aArr[msk].astype(np.float32) + (a * 255), t)
                        self.pixArr[msk] = (self.pixArr[msk] * (t / 255 - a)[..., None] + a[..., None] * self.color) / (t[..., None] / 255)
                        self.aArr[msk] = t.astype(np.uint32)
        del self.pixArr
        del self.aArr
        
        screen.blit(self.surf, (self.rect.x, self.rect.y))
        
