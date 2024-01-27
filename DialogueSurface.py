import os
# import basic pygame modules
import pygame as pg

import numpy as np

import pygame_widgets

main_dir = os.path.split(os.path.abspath(__file__))[0]

class Text:
    def __init__(self, text, rect, fontName = None, fontSize = 20):
        self.text = text
        self.rect = rect
        if (fontName is None):
            fontName = pg.font.get_default_font()
        self.font = pg.font.SysFont("Arial", fontSize)
        self.renderedText = self.font.render(self.text, True, "black")
        
    def update(self, surface): #TODO this needs to deal with multiline stuff and scrolling
        surface.unlock()
        self.renderedText.unlock()
        surface.blit(self.renderedText, (0, 0))

#TODO needs to render animated components

#this handles overall placement and stuff like scroll buttons
class DialogueSurface:
    def __init__(self, parent, position):
        self.rect = position
        
        self.surf = parent.subsurface(self.rect)
        self.surf.fill(pg.Color("grey"))
        
        self.text = None
        
    
    def setText(self, text):
        self.text = Text(text, self.rect)
    
    def update(self, screen):
        if (self.text is not None):
            self.text.update(self.surf)
    