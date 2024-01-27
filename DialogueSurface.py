import pygame as pg
import time

class Line:
    
    def __init__(self, font, line, spacing, animationRules = []):
        self.font = font
        self.line = line
        self.spacing = spacing
        self.animationRules = animationRules
        
        self.width, self.height = self.font.size(self.line)
        self.surf = self.font.render(self.line, True, "black", "grey")
        
    def fits(self, rect, offset):
        return rect.w > offset[0] + self.width and rect.h > offset[1] + self.height
    
#TODO needs to render animated components
    def renderLine(self, surface, offset):
            surface.blit(self.surf, (offset[0], offset[1]))

class Text:
    def __init__(self, text, rect, fontName = None, fontSize = 20):
        self.text = text
        self.rect = rect
        if (fontName is None):
            fontName = pg.font.get_default_font()
        self.font = pg.font.SysFont("Arial", fontSize)
        
        #render Text
        split_string = [s.strip() for s in self.text.split(" ") if len(s.strip()) > 0]
        
        self.linePos = 0
        self.lines = [""]
        while (len(split_string) > 0):
            w, _ = self.font.size(self.lines[-1] + " " + split_string[0])
            if w < self.rect.w:
                self.lines[-1] = self.lines[-1] + " " + split_string[0]
            else:
                self.lines.append("")
            split_string = split_string[1:]
        
        self.lines = [Line(self.font, l, 5, []) for l in self.lines[:-1]]
        
        
        self.lastT = time.monotonic()
        
    def update(self, surface):
        currHeight = 0
        lineCounter = 0
        while (lineCounter + self.linePos) < len(self.lines):
            line = self.lines[lineCounter + self.linePos]
            if not line.fits(self.rect, (0, currHeight)):
                break
            line.renderLine(surface, (0, currHeight))
            currHeight += line.height + line.spacing
            lineCounter += 1
        
        if (time.monotonic() - self.lastT) > 0.8:
            self.lastT = time.monotonic()
            if (self.linePos < (len(self.lines) - 1)):
                self.linePos += 1


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
        self.surf.fill(pg.Color("grey"))
        if (self.text is not None):
            self.text.update(self.surf)
    