import pygame as pg
from DrawUtil import load_image
import json

class CharacterSurface:
    
    def __init__(self, position, image, positionMap, shirt = None, shoe = None, pants = None):
        
        self.pos = position
        self.setCharacter(image)
        with open("./Data/person.json", "r") as f:
            self.map = json.load(f)
            
        self.shirt = shirt
        if (shirt is not None):
            dressShirt(shirt)
        self.shoe = shoe #transform
        #self.shoe = pg.transform.scale(self.shoe, self.map["shoe"]["size"])
        self.pants = pants #transform
        #self.pants = pg.transform.scale(self.pants, self.map["pants"]["size"])
        
    
    def setCharacter(self, image):
        self.imageName = image[1 + image.rfind("/") : image.rfind(".")]
        image = load_image(image)
        
        self.sze = image.get_size()
        image = pg.transform.scale(image, (self.pos.w, self.pos.h))
        self.image = pg.Surface((self.pos.w, self.pos.h), pg.SRCALPHA)
        self.image.blit(image,(0, 0))
        
        pixArr = pg.surfarray.pixels3d(self.image)
        aArr = pg.surfarray.pixels_alpha(self.image)
        pixArr[pixArr[..., 1] > (pixArr[..., 0] + pixArr[..., 2])] = (127, 86, 2)
        aArr[(pixArr[..., 1] + pixArr[..., 0] + pixArr[..., 2]) > 0] = 196
        aArr[(pixArr[..., 1] + pixArr[..., 0] + pixArr[..., 2]) == 0] = 0
        del pixArr
        del aArr
        
        self.shirt = None
        self.pants = None
        self.shoe = None
    
    def transformFromImgToSurf(self, p):
        x, y = p
        return (x * self.pos.w / self.sze[0], y * self.pos.h / self.sze[1])
    
    def dressShirt(self, image):
        self.shirt = image #transform
        self.shirt = pg.transform.scale(self.shirt, self.map[self.imageName]["shirt"]["size"])
        self.shirt = pg.transform.scale(self.shirt, self.transformFromImgToSurf(self.map[self.imageName]["shirt"]["size"]))
    
    def update(self, surface, state):
        surface.blit(self.image, self.pos)
        absOff = surface.get_abs_offset()
        map = self.map[self.imageName]
        if self.shoe is not None:
            off = self.transformFromImgToSurf(map["shoe"]["offset"][0])
            surface.blit(self.shoe, (off[0] + absOff[0] + self.pos[0], off[1] + absOff[1] + self.pos[1]))
            off = self.transformFromImgToSurf(map["shoe"]["offset"][1])
            surface.blit(self.shoe, (off[0] + absOff[0] + self.pos[0], off[1] + absOff[1] + self.pos[1]))
        if self.pants is not None:
            off = self.transformFromImgToSurf(map["pants"]["offset"])
            surface.blit(self.pants, (off[0] + absOff[0] + self.pos[0], off[1] + absOff[1] + self.pos[1]))
        if self.shirt is not None:
            off = self.transformFromImgToSurf(map["shirt"]["offset"])
            surface.blit(self.shirt, (off[0] + absOff[0] + self.pos[0], off[1] + absOff[1] + self.pos[1]))