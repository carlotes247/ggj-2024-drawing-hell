import pygame as pg
from DrawUtil import load_image
import json

class CharacterSurface:
    
    def __init__(self, position, image, positionMap, shirt = None, shoe = None, pants = None):
        
        self.pos = position
        self.image = load_image(image)
        
        self.sze = self.image.get_size()
        self.image = pg.transform.scale(self.image, (position.w, position.h))
        with open(positionMap, "r") as f:
            self.map = json.load(f)
            
        self.shirt = shirt
        if (shirt is not None):
            dressShirt(shirt)
        self.shoe = shoe #transform
        #self.shoe = pg.transform.scale(self.shoe, self.map["shoe"]["size"])
        self.pants = pants #transform
        #self.pants = pg.transform.scale(self.pants, self.map["pants"]["size"])
        
    
    def transformFromImgToSurf(self, p):
        x, y = p
        return (x * self.pos.w / self.sze[0], y * self.pos.h / self.sze[1])
    
    def dressShirt(self, image):
        self.shirt = image #transform
        self.shirt = pg.transform.scale(self.shirt, self.transformFromImgToSurf(self.map["shirt"]["size"]))
    
    def update(self, surface):
        surface.blit(self.image, self.pos)
        absOff = surface.get_abs_offset()
        if self.shoe is not None:
            off = self.transformFromImgToSurf(self.map["shoe"]["offset"][0])
            surface.blit(self.shoe, (off[0] + absOff[0] + self.pos[0], off[1] + absOff[1] + self.pos[1]))
            off = self.transformFromImgToSurf(self.map["shoe"]["offset"][1])
            surface.blit(self.shoe, (off[0] + absOff[0] + self.pos[0], off[1] + absOff[1] + self.pos[1]))
        if self.pants is not None:
            off = self.transformFromImgToSurf(self.map["pants"]["offset"])
            surface.blit(self.pants, (off[0] + absOff[0] + self.pos[0], off[1] + absOff[1] + self.pos[1]))
        if self.shirt is not None:
            off = self.transformFromImgToSurf(self.map["shirt"]["offset"])
            surface.blit(self.shirt, (off[0] + absOff[0] + self.pos[0], off[1] + absOff[1] + self.pos[1]))