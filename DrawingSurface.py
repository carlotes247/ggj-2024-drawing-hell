import os
# import basic pygame modules
import pygame as pg

import numpy as np

import pygame_widgets

main_dir = os.path.split(os.path.abspath(__file__))[0]


class DrawSurface:
    
    def __init__(self, parent, position):
        
        self.rect = position
        
        self.surf = pg.Surface((self.rect.w, self.rect.h))
        self.surf.fill([255, 255, 255, 255])
        self.idxArr = np.mgrid[:self.rect.w, : self.rect.h]
        
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
    
    def getResultImage(self):
        pixArr = pg.surfarray.pixels3d(self.surf)
        area = self.idxArr[:, (pixArr[..., 0] < 255) & (pixArr[..., 1] < 255) & (pixArr[..., 2] < 255)]
        minX, minY = np.min(area[0]), np.min(area[1])
        maxX, maxY = np.max(area[0]), np.max(area[1])
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
    
    def update(self, screen):
        mouse_pressed = pg.mouse.get_pressed(num_buttons = 3)
        pos = pg.mouse.get_pos()
        if (self.rect.collidepoint(pos)):
            self.pixArr = pg.surfarray.pixels3d(self.surf)
            drawPos = (pos[0] - self.rect.x, pos[1] - self.rect.y)
            if (mouse_pressed[2]): #right button pressed
                radius = self.getDist(drawPos)
                msk = radius < self.size
                self.pixArr[msk] = [255, 255, 255]
            elif (mouse_pressed[0]): #leftbutton pressed
                radius = self.getDist(drawPos)
                msk = radius < self.size
                a = ((self.size - radius[msk]) / self.size)[:, None]
                self.pixArr[msk] = self.pixArr[msk] * (1 - a) + a * self.color
            del self.pixArr
        
        screen.blit(self.surf, (self.rect.x, self.rect.y))
        


#def main(winstyle=0):
    #toolkitRect = pg.Rect(SCREENRECT.size[0] * 0.05, SCREENRECT.size[1] * 0.1, SCREENRECT.size[0] * 0.2, SCREENRECT.size[1] * 0.65)
    #toolkitSurface = screen.subsurface(toolkitRect)
    #toolkitSurface.fill(pg.Color("grey"))
    
    #r_slider = Slider(toolkitSurface, 10, 20, SCREENRECT.size[0] * 0.2 - 20, 20, min=0, max=255, step=1)
    #g_slider = Slider(toolkitSurface, 10, 60, SCREENRECT.size[0] * 0.2 - 20, 20, min=0, max=255, step=1)
    #b_slider = Slider(toolkitSurface, 10, 100, SCREENRECT.size[0] * 0.2 - 20, 20, min=0, max=255, step=1)
    #rgb_text = TextBox(toolkitSurface, 10, 140, SCREENRECT.size[0] * 0.2 - 20, 20, fontSize=15)
    #rgb_text.disable()
    
    #test_button = Button(toolkitSurface, 10, 180, SCREENRECT.size[0] * 0.2 - 20, 20, text="test", onClick = lambda: print("clicked"))
    