import os
import pygame as pg

def load_image(file):
    """loads an image, prepares it for play"""
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert()

def drawRoundedRect(surface, rect, color, rounded = 0):
    if (rounded <= 0):
        pg.draw.rect(surface, color, rect)
    else:
        renderRect = rect.copy()
        renderRect.h -= rounded * 2
        renderRect.y += rounded
        pg.draw.rect(surface, color, renderRect)
        renderRect = rect.copy()
        renderRect.w -= rounded * 2
        renderRect.x += rounded
        pg.draw.rect(surface, color, renderRect)
        
        xOff = rect.x + rounded
        yOff = rect.y + rounded
        pg.draw.circle(surface, color, (xOff, yOff), rounded)
        
        xOff1 = rect.x + rect.w - rounded
        pg.draw.circle(surface, color, (xOff1, yOff), rounded)
        
        yOff = rect.y + rect.h - rounded
        pg.draw.circle(surface, color, (xOff, yOff), rounded)
        pg.draw.circle(surface, color, (xOff1, yOff), rounded)
        