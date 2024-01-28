import pygame as pg
import functools
import  random

from DrawingSurface import DrawSurface
from DialogueSurface import DialogueSurface, Line
from CharacterView import CharacterSurface
from GraveStone import Gravestone
from CustomButton import Button
from DialogueState import DialogueState
from State import State
from DrawUtil import *
# see if we can load more than standard BMP
if not pg.image.get_extended():
    raise SystemExit("Sorry, extended image module required")

# game constants
SCREENRECT = pg.Rect(0, 0, 1366, 768)
CENTER = (SCREENRECT.w // 2, SCREENRECT.h // 2)
QUARTER = (SCREENRECT.w // 4, SCREENRECT.h // 4)
DRAWRECT = pg.Rect(QUARTER[0], QUARTER[1], CENTER[0], CENTER[1])
CHARRECT = pg.Rect(16, QUARTER[1] / 2, QUARTER[0] - 32, CENTER[1] + 24 + QUARTER[1] / 2)
DIAGRECT = pg.Rect(QUARTER[0], QUARTER[1] + CENTER[1] + 48, CENTER[0], QUARTER[1] - 96)
GRAVERECT = pg.Rect(48, QUARTER[1] + CENTER[1] + 8 - 32, QUARTER[0] - 96, QUARTER[1] + 32)


SELECTRECT = pg.Rect(CENTER[0] + QUARTER[0] + 32, QUARTER[1] / 2, QUARTER[0] - 64, CENTER[1] + QUARTER[1])

BackgroundImage = None
SubmitButton = None

def init():
    # Initialize pygame
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()
    if pg.mixer and not pg.mixer.get_init():
        print("Warning, no sound")
        pg.mixer = None
        
    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pg.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pg.display.set_mode(SCREENRECT.size, winstyle | pg.SRCALPHA, bestdepth)
    
    # decorate the game window
    pg.display.set_caption("Pygame Demo")
    pg.mouse.set_visible(1)

    # create the background, tile the bgd image
    screen = pg.display.set_mode( SCREENRECT.size )
    screen.fill(pg.Color("white"))
    pg.display.flip()
    screen.unlock()
    return screen


def initDrawingSurface(surf):
    res = DrawSurface(surf, pg.Rect(DRAWRECT.x + 16, DRAWRECT.y + 16 + 48, DRAWRECT.w - 48, DRAWRECT.h - 96))
    return res

def initDialogueSurface(surf):
    res = DialogueSurface(surf, DIAGRECT)
    res.setText("Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.")
    return res

def initCharacterSurface(surf):
    res = CharacterSurface(pg.Rect(CHARRECT.x, CHARRECT.y, CHARRECT.w, CHARRECT.h), "./Data/person.png", "./Data/person.json")
    res.setCharacter("./Data/personShape1.png")
    return res

def drawBG(surf):
    surf.blit(BackgroundImage, (0, 0)) #background image
    
    drawRoundedRect(surf, DRAWRECT, "white", 48)
    drawRoundedRect(surf, pg.Rect(SELECTRECT.x, SELECTRECT.y, SELECTRECT.w, SELECTRECT.h), pg.Color(162, 126, 144), 48)
    


def generateButtons(surf, DrawingSurf, diagSurf, ):
    
    diagWid = SELECTRECT.w / 5
    selectCenter = SELECTRECT.x + SELECTRECT.w / 2
    selectCenterH = SELECTRECT.y + SELECTRECT.h / 2
    
    topColorLine = 80
    secondColorLine = 140
    
    l1 = [
    Button("", pg.Rect(selectCenter - diagWid - 12, selectCenterH + 18, 16, 16), lambda state, clicked, held : DrawingSurf.setSize(8) if clicked and not held else 0, rounded = 8),
    Button("", pg.Rect(selectCenter - 18, selectCenterH + 14, 24, 24), lambda state, clicked, held : DrawingSurf.setSize(12) if clicked and not held else 0, rounded = 12),
    Button("", pg.Rect(selectCenter + diagWid - 20, selectCenterH + 10, 32, 32), lambda state, clicked, held : DrawingSurf.setSize(16) if clicked and not held else 0, rounded = 16)
    ]
    
    ref = functools.partial(updateColor, l1, DrawingSurf)
    
    l = [
    Button("CLEAR", pg.Rect(selectCenter - 100, QUARTER[1] + CENTER[1] - 18, 200, 50), lambda state, clicked, held : DrawingSurf.clear() if clicked and not held else 0, rounded = 25, fontSize = 24, color = pg.Color(162, 126, 144), clickColor = pg.Color(82, 32, 82), fontColor = "white"),
    Button("SUBMIT", pg.Rect(selectCenter - 100, QUARTER[1] + CENTER[1] + 32, 200, 50), lambda state, clicked, held : pg.event.post(pg.event.Event(state.SUBMIT_EVENT)) if clicked and not held else 0, rounded = 25, fontSize = 24, color = pg.Color(162, 126, 144), clickColor = pg.Color(82, 32, 82), fontColor = "white"),
    Button("", pg.Rect(selectCenter - diagWid - 24, SELECTRECT.y + topColorLine, 48, 48), lambda state, clicked, held : ref(clicked, held, (0, 89, 109)), color = pg.Color(0, 89, 109), rounded = 24),
    Button("", pg.Rect(selectCenter - 24, SELECTRECT.y + topColorLine, 48, 48), lambda state, clicked, held : ref(clicked, held, (232, 151, 46)), color = pg.Color(232, 151, 46), rounded = 24),
    Button("", pg.Rect(selectCenter + diagWid - 24, SELECTRECT.y + topColorLine, 48, 48), lambda state, clicked, held : ref(clicked, held, (255, 236, 167)), color = pg.Color(255, 236, 167), rounded = 24),
    Button("", pg.Rect(selectCenter - diagWid - 24, SELECTRECT.y + secondColorLine, 48, 48), lambda state, clicked, held : ref(clicked, held, (183,226,170)), color = pg.Color(183,226,170), rounded = 24),
    Button("", pg.Rect(selectCenter - 24, SELECTRECT.y + secondColorLine, 48, 48), lambda state, clicked, held : ref(clicked, held, (157,98,98)), color = pg.Color(157,98,98), rounded = 24),
    Button("", pg.Rect(selectCenter + diagWid - 24, SELECTRECT.y + secondColorLine, 48, 48), lambda state, clicked, held : ref(clicked, held, (1,8,18)), color = pg.Color(1,8,18), rounded = 24),
    ]
    l.extend(l1)
    
    font = pg.font.Font("./Data/ARCADE_N.TTF", 24)
    
    line = Line(font, "Color", 0, txtColor = "white", bgColor = pg.Color(162, 126, 144))
    line.offset = (selectCenter - line.width / 2, SELECTRECT.y + 20)
    l.append(line)
    line = Line(font, "Brush", 0, txtColor = "white", bgColor = pg.Color(162, 126, 144))
    line.offset = (selectCenter - line.width / 2, selectCenterH - 50)
    l.append(line)
    
    
    line = Line(font, "Your Design", 0, txtColor = pg.Color(82, 32, 82), bgColor = "white")
    line.offset = (DRAWRECT.x + DRAWRECT.w / 2 - line.width / 2, DRAWRECT.y + 24)
    l.append(line)
    
    return l
    
def updateColor(l, DrawingSurf, click, held, color):
    if click and not held:
        for i in l:
            i.color = color
        DrawingSurf.setColor(color)

def run(screen, draw, state, characterSurface, grave, updatables):
    
    clock = pg.time.Clock()
    
    # Run our main loop whilst the player is alive.
    while True:
        events = pg.event.get()
        # get input
        for event in events:
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return
            if event.type == state.SUBMIT_EVENT:
                state.diag.checkResponse()
                characterSurface.dressShirt(draw.getResultImage())
                pg.time.set_timer(pg.event.Event(state.NEW_CHARACTER_EVENT), 2000, loops = 1)
            elif event.type == state.NEW_CHARACTER_EVENT:
                state.diag.request()
                draw.clear()
                characterSurface.setCharacter(random.choice(["./Data/personShape1.png", "./Data/personShape2.png", "./Data/personShape3.png"]))
                grave.generate(state)
        
        drawBG(screen)
        
        #update calls
        for u in updatables:
            u.update(screen, state)
        
        #pygame_widgets.update(events)
        #pg.display.update(toolkitRect)
        pg.display.flip() #render call

        # cap the framerate at 40fps. Also called 40HZ or 40 times per second.
        clock.tick(60)
    

def quit():
    pg.quit()


if __name__ == "__main__":
    screen = init()
    
    
    BackgroundImage = load_image("./data/background.png")
    BackgroundImage = pg.transform.scale(BackgroundImage, (SCREENRECT.w, SCREENRECT.h))
    
    draw = initDrawingSurface(screen)
    diag = initDialogueSurface(screen)
    char = initCharacterSurface(screen)
    grave = Gravestone(GRAVERECT)
    state = State(DialogueState("./Data/dialogue.json", diag))
    lst = generateButtons(screen, draw, diag)
    lst.append(draw)
    lst.append(diag)
    lst.append(char)
    lst.append(grave)
    pg.time.set_timer(pg.event.Event(state.NEW_CHARACTER_EVENT), 10, loops = 1)
    run(screen, draw, state, char, grave, lst)
    quit()