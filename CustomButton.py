import pygame as pg
from DrawUtil import drawRoundedRect
class Button:
    def __init__(self, text, rect, callback, color = "grey", clickColor = "grey", rounded = 0, fontColor = "black", fontName = None, fontSize = 6):
        self.text = text
        self.rect = rect
        self.callback = callback
        self.color = color
        self.clickColor = clickColor
        self.rounded = rounded
        self.fontColor = fontColor
        
        self.font = pg.font.Font("./Data/ARCADE_N.TTF", fontSize)
        
        self.renderedText = self.font.render(self.text, True, fontColor, color)
        self.clickRenderedText = self.font.render(self.text, True, fontColor, clickColor)
        self.textWidth, self.textHeight = self.font.size(self.text)
        
        self.clicked = True
        
        
    def update(self, surface, state):
        
        #handle clicking
        pos = pg.mouse.get_pos()
        absOff = surface.get_abs_offset()
        pos = (pos[0] - absOff[0], pos[1] - absOff[1])
        if (self.rect.collidepoint(pos)):
            c = pg.mouse.get_pressed(num_buttons = 3)[0]
            
            if (c and not self.clicked):
                self.callback(state, True, False)
            self.clicked = c
        else:
            self.clicked = False
            self.callback(state, False, False)
        
        bgColor = self.color
        txt = self.renderedText
        if (self.clicked):
            bgColor = self.clickColor
            txt = self.clickRenderedText
            self.callback(state, False, True)
        #render background
        drawRoundedRect(surface, self.rect, bgColor, self.rounded)
        #render text
        xOff = self.rect.x + (self.rect.w - self.textWidth) / 2
        yOff = self.rect.y + (self.rect.h - self.textHeight) / 2
        surface.blit(txt, (xOff, yOff))