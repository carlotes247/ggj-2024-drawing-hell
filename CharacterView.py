import pygame as pg
from DrawUtil import load_image
import json
import numpy as np

class CharacterSurface:
    
    def __init__(self, position, positionMap, clothes = {}):
        
        self.pos = position
        with open("./Data/person.json", "r") as f:
            self.map = json.load(f)
            
        self.clothes = {}
        for k, v in clothes.items():
            self.dressCloth(v, k)
        
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
        
        self.clothes = {}
    
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
    
    def dressCloth(self, image, type):
        self.clothes[type] = image #transform
        sze = self.map[self.imageName][type]["size"]
        self.clothes[type] = pg.transform.scale(self.clothes[type], (sze[0] * 2, sze[1] * 2))
        self.clothes[type] = pg.transform.scale(self.clothes[type], self.transformFromImgToSurf(self.map[self.imageName][type]["size"]))
    
    def update(self, surface, state):
        surface.blit(self.image, self.pos)
        
        absOff = surface.get_abs_offset()
        if (self.highlight is not None):
            off = self.transformFromImgToSurf(self.map[self.imageName][self.highlight]["offset"])
        
            surface.blit(self.highlightRect, (off[0] + absOff[0] + self.pos[0], off[1] + absOff[1] + self.pos[1]))
        
        map = self.map[self.imageName]
        
        for k, v in self.clothes.items():
            if v is None:
                continue
            off = self.transformFromImgToSurf(map[k]["offset"])
            surface.blit(v, (off[0] + absOff[0] + self.pos[0], off[1] + absOff[1] + self.pos[1]))
        