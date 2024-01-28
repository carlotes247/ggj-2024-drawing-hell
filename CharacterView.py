import pygame as pg
from DrawUtil import load_image
import json
import numpy as np

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
        
        self.highlight = None
        self.highlightRect = pg.Surface((32, 32), pg.SRCALPHA)
        self.highlightRect.fill((255, 255, 255, 24))
        
        
    
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
        
        
        sze = aArr.shape
        
        ySze = sze[1] / 4
        
        y, x = np.mgrid[-sze[0] / 2:sze[0] / 2,-ySze:sze[1]  -ySze]
        weights = ((x ** 2) / (sze[1] ** 2 / 4)) + ((y ** 2) / (sze[0] ** 2 / 4))
        weights = np.clip((1.0 - weights), 0.6, 1)
        
        aArr[True] = (aArr.astype(np.float32) * weights).astype(np.uint8)
        
        del pixArr
        del aArr
        
        self.shirt = None
        self.pants = None
        self.shoe = None
    
    def transformFromImgToSurf(self, p):
        x, y = p
        return (x * self.pos.w / self.sze[0], y * self.pos.h / self.sze[1])
    
    def getCharCrop(self, type):
        off = self.transformFromImgToSurf(self.map[self.imageName][type]["offset"])
        sze = self.transformFromImgToSurf(self.map[self.imageName][type]["size"])
        #handle shoes
        sur = pg.Surface(sze, pg.SRCALPHA)
        sur.blit(self.image, (0,0), area = (off[0], off[1], sze[0], sze[1]))
        aArr = pg.surfarray.pixels_alpha(sur)
        pixArr = pg.surfarray.pixels3d(sur)
        aArr[True] = 24
        aArr[(pixArr[..., 1] + pixArr[..., 0] + pixArr[..., 2]) == 0] = 0
        del aArr
        del pixArr
        return sur
    
    def setHighlightArea(self, type):
        sze = self.transformFromImgToSurf(self.map[self.imageName][type]["size"])
        self.highlight = type
        self.highlightRect = pg.transform.scale(self.highlightRect, sze)
    
    def dressShirt(self, image):
        self.shirt = image #transform
        sze = self.map[self.imageName]["shirt"]["size"]
        self.shirt = pg.transform.scale(self.shirt, (sze[0] * 2, sze[1] * 2))
        self.shirt = pg.transform.scale(self.shirt, self.transformFromImgToSurf(self.map[self.imageName]["shirt"]["size"]))
    
    def update(self, surface, state):
        surface.blit(self.image, self.pos)
        
        absOff = surface.get_abs_offset()
        if (self.highlight is not None):
            off = self.transformFromImgToSurf(self.map[self.imageName][self.highlight]["offset"])
        
            surface.blit(self.highlightRect, (off[0] + absOff[0] + self.pos[0], off[1] + absOff[1] + self.pos[1]))
        
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