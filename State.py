import pygame as pg

class State:
    
    def __init__(self, diagObj):
        self.NEW_CHARACTER_EVENT = pg.event.custom_type()
        self.SUBMIT_EVENT = pg.event.custom_type()
        self.diag = diagObj