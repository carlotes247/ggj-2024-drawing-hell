import pygame as pg
from DrawUtil import load_image
from  DialogueSurface import Text
import json
import json
import random

class Gravestone:
    
    dataSet = None
    
    def __init__(self, position):
        
        if (Gravestone.dataSet is None):
            with open("./Data/graveData.json", "r") as f:
                Gravestone.dataSet = json.load(f)
        
        
        self.pos = position
        baseImage = load_image("./Data/grave.png")
        baseImage = pg.transform.scale(baseImage, (self.pos.w, self.pos.h))
        self.baseImage = pg.Surface((self.pos.w, self.pos.h), pg.SRCALPHA)
        self.baseImage.blit(baseImage,(0, 0))
        
        #clean image and fit
        self.colorGravestone()
        
        self.nameFont = pg.font.Font("./Data/ARCADE_N.TTF", 20)
        
        self.deathCause = Text("", pg.Rect(30, 90, position.w, position.h), fontSize =  12, txtColor = "black", bgColor = None)
        
        self.colorGravestone()
        self.generate()
    
    def colorGravestone(self):
        pixArr = pg.surfarray.pixels3d(self.baseImage)
        aArr = pg.surfarray.pixels_alpha(self.baseImage)
        pixArr[pixArr[..., 1] > (pixArr[..., 0] + pixArr[..., 2])] = (86, 86, 86)
        aArr[(pixArr[..., 1] + pixArr[..., 0] + pixArr[..., 2]) > 0] = 255
        aArr[(pixArr[..., 1] + pixArr[..., 0] + pixArr[..., 2]) == 0] = 0
        del pixArr
        del aArr
        
    
    def generate(self):
        name = random.choice(["maleNames", "femaleNames"])
        name = random.choice(Gravestone.dataSet[name])
        self.firstName = self.nameFont.render(name, True, "black", (86, 86, 86))
        self.deathCause.setText(random.choice(Gravestone.dataSet["deathCauses"]))
        
        w, _ = self.nameFont.size(name)
        
        self.image = self.baseImage.copy()
        self.image.blit(self.firstName, (self.pos.w / 2 - w / 2, 50))
        self.deathCause.update(self.image)
    
    def update(self, surface):
        
        surface.blit(self.image, (self.pos.x, self.pos.y))
        
        