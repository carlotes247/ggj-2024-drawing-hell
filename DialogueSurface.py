import pygame as pg
import time
from DrawUtil import drawRoundedRect

from CustomButton import Button

class Line:
    def __init__(self, font, line, spacing, offset = None, txtColor = "black", bgColor = "grey", animationRules = []):
        self.offset = offset
        
        self.font = font
        self.line = line
        self.spacing = spacing
        self.animationRules = animationRules
        
        self.width, self.height = self.font.size(self.line)
        self.surf = self.font.render(self.line, True, txtColor, bgColor)
        
    def fits(self, rect, offset):
        return rect.w > offset[0] + self.width and rect.h > offset[1] + self.height
    
    def update(self, surf, state):
        if self.offset is not None:
            self.renderLine(surf, self.offset)
    
    #TODO needs to render animated components
    def renderLine(self, surface, offset):
            surface.blit(self.surf, (offset[0], offset[1]))

class Text:
    def __init__(self, text, rect, fontName = None, fontSize = 10, txtColor = "black", bgColor = "grey"):
        self.rect = rect
        self.font = pg.font.Font("./Data/ARCADE_N.TTF", fontSize)
        self.lastT = time.monotonic()
        self.txtColor = txtColor
        self.bgColor = bgColor
        self.setText(text)
        
    def setText(self, text):
        self.text = text
        #render Text
        split_string = [s.strip() for s in self.text.split(" ") if len(s.strip()) > 0]
        
        self.linePos = 0
        self.lines = [""]
        while (len(split_string) > 0):
            w, _ = self.font.size(self.lines[-1] + " " + split_string[0])
            if (w + self.rect.x) < (self.rect.w - self.rect.x):
                self.lines[-1] = self.lines[-1] + " " + split_string[0]
                split_string = split_string[1:]
            else:
                self.lines.append("")
        
        self.lines = [Line(self.font, l, 5, offset = (self.rect.x, self.rect.y), txtColor = self.txtColor, bgColor = self.bgColor) for l in self.lines]
    
    def scroll(self):
        if (self.linePos < (len(self.lines) - 1)):
            self.linePos += 1
    
    def update(self, surface, state):
        currHeight = self.rect.y
        lineCounter = 0
        while (lineCounter + self.linePos) < len(self.lines):
            line = self.lines[lineCounter + self.linePos]
            if not line.fits(self.rect, (0, currHeight)):
                break
            line.renderLine(surface, (self.rect.x, currHeight))
            currHeight += line.height + line.spacing
            lineCounter += 1
        
        if (time.monotonic() - self.lastT) > 0.8:
            self.lastT = time.monotonic()
            #self.scroll()


#this handles overall placement and stuff like scroll buttons
class DialogueSurface:
    def __init__(self, parent, position, bgColor = "grey", txtColor = "black", rounded = 4):
        self.rect = position
        
        self.surf = parent.subsurface(self.rect)
        self.rounded = rounded
        self.bgColor = bgColor
        drawRoundedRect(self.surf, pg.Rect(0, 0, self.rect.w, self.rect.h), color = self.bgColor, rounded = self.rounded)
        #self.surf.fill(pg.Color("grey"))
        
        self.text = None
        
        self.nextBtn = Button(">", pg.Rect(self.rect.w - 30, self.rect.h - 30, 20, 20), lambda state, clicked, held : self.scroll() if (clicked and not held) else 0, color = bgColor, fontColor = txtColor)
        self.text = Text("", pg.Rect(10, 15, self.rect.w, self.rect.h - 30), bgColor = bgColor, txtColor = txtColor)
        
    
    def scroll(self):
        if self.text is not None:
            self.text.scroll()
    
    def setText(self, text):
        self.text.setText(text)
    
    def update(self, screen, state):
        drawRoundedRect(self.surf, pg.Rect(0, 0, self.rect.w, self.rect.h), color = self.bgColor, rounded = self.rounded)
        self.nextBtn.update(self.surf, state)
        if (self.text is not None):
            self.text.update(self.surf, state)
    