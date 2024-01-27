import os
# import basic pygame modules
import pygame as pg

import numpy as np

import pygame_widgets

main_dir = os.path.split(os.path.abspath(__file__))[0]


class DrawSurface:
    
    def __init__(self, parent, position):
        
        self.rect = position
        
        self.surf = parent.subsurface(self.rect)
        self.surf.fill([0, 0, 0, 255])
        self.surf.fill(pg.Color("black"))
        
        self.pixArr = pg.surfarray.pixels3d(self.surf)
        self.idxArr = np.mgrid[:self.pixArr.shape[0], : self.pixArr.shape[1]]
        
    def getDist(self, pos):
        iArr = self.idxArr.copy()
        iArr[0] -= pos[0]
        iArr[1] -= pos[1]
        
        iArr = np.power(iArr, 2)
        
        return np.sum(iArr, axis = 0 )
    
    def update(self):
        mouse_pressed = pg.mouse.get_pressed(num_buttons = 3)
        pos = pg.mouse.get_pos()
        if (self.rect.collidepoint(pos)):
            drawPos = (pos[0] - self.rect.x, pos[1] - self.rect.y)
            if (mouse_pressed[2]): #right button pressed
                radius = self.getDist(drawPos)
                msk = radius < 144
                self.pixArr[msk] = 0
            elif (mouse_pressed[0]): #leftbutton pressed
                radius = self.getDist(drawPos)
                msk = radius < 144
                a = ((144 - radius[msk]) / 144)[:, None]
                self.pixArr[msk] = self.pixArr[msk] * (1 - a) + a * 255
        


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
    