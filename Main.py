import pygame as pg
from DrawingSurface import DrawSurface
from DialogueSurface import DialogueSurface
from CustomButton import Button
from DrawUtil import *
# see if we can load more than standard BMP
if not pg.image.get_extended():
    raise SystemExit("Sorry, extended image module required")

# game constants
SCREENRECT = pg.Rect(0, 0, 800, 600)
DRAWRECT = pg.Rect(SCREENRECT.size[0] * 0.2, SCREENRECT.size[1] * 0.1, SCREENRECT.size[0] * 0.45, SCREENRECT.size[1] * 0.7)
DIALOGUERECT = pg.Rect(SCREENRECT.size[0] * 0.65 + 80, SCREENRECT.size[1] * 0.1, SCREENRECT.size[0] * 0.35 - 120, SCREENRECT.size[1] * 0.7)

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
    res = DrawSurface(surf, DRAWRECT)
    return res

def initDialogueSurface(surf):
    res = DialogueSurface(surf, DIALOGUERECT)
    res.setText("Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.")
    return res

def drawBG(surf):
    surf.blit(BackgroundImage, (0, 0)) #background image
    SubmitButton.update(surf)
    
    drawRoundedRect(surf, pg.Rect(DRAWRECT.x - 8, DRAWRECT.y - 8, DRAWRECT.w + 16, DRAWRECT.h + 16), "blue", 24)
    drawRoundedRect(surf, pg.Rect(DIALOGUERECT.x - 8, DIALOGUERECT.y - 8, DIALOGUERECT.w + 16, DIALOGUERECT.h + 16), "red", 24)
    

def generateButtons(surf, DrawingSurf):
    
    diagWid = DIALOGUERECT.w / 5
    return [
    Button("", pg.Rect(DIALOGUERECT.x + diagWid * 1, DIALOGUERECT.y + 80, 32, 32), lambda clicked, held : DrawingSurf.setColor((255, 0, 0)) if clicked and not held else 0, rounded = 16),
    Button("", pg.Rect(DIALOGUERECT.x + diagWid * 2, DIALOGUERECT.y + 80, 32, 32), lambda clicked, held : DrawingSurf.setColor((255, 0, 0)) if clicked and not held else 0, rounded = 16),
    Button("", pg.Rect(DIALOGUERECT.x + diagWid * 3, DIALOGUERECT.y + 80, 32, 32), lambda clicked, held : DrawingSurf.setColor((255, 0, 0)) if clicked and not held else 0, rounded = 16),
    Button("", pg.Rect(DIALOGUERECT.x + diagWid * 1, DIALOGUERECT.y + 120, 32, 32), lambda clicked, held : DrawingSurf.setColor((255, 0, 0)) if clicked and not held else 0, rounded = 16),
    Button("", pg.Rect(DIALOGUERECT.x + diagWid * 2, DIALOGUERECT.y + 120, 32, 32), lambda clicked, held : DrawingSurf.setColor((255, 0, 0)) if clicked and not held else 0, rounded = 16),
    Button("", pg.Rect(DIALOGUERECT.x + diagWid * 3, DIALOGUERECT.y + 120, 32, 32), lambda clicked, held : DrawingSurf.setColor((255, 0, 0)) if clicked and not held else 0, rounded = 16),
    
    Button("", pg.Rect(DIALOGUERECT.x + diagWid * 2 + 16, DIALOGUERECT.y + 200, 16, 16), lambda clicked, held : DrawingSurf.setSize(8) if clicked and not held else 0, rounded = 8),
    Button("", pg.Rect(DIALOGUERECT.x + diagWid * 2 + 8, DIALOGUERECT.y + 220, 32, 32), lambda clicked, held : DrawingSurf.setSize(16) if clicked and not held else 0, rounded = 16),
    Button("", pg.Rect(DIALOGUERECT.x + diagWid * 2, DIALOGUERECT.y + 260, 48, 48), lambda clicked, held : DrawingSurf.setSize(24) if clicked and not held else 0, rounded = 24)]
    

def run(screen, updatables):
    
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
        
        drawBG(screen)
        
        #update calls
        for u in updatables:
            u.update(screen)
        
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
    
    SubmitButton = Button("SUBMIT", pg.Rect(SCREENRECT.size[0] * 0.2, SCREENRECT.size[1] * 0.8 + 32, 120, 40), lambda clicked, held : 0, rounded = 8)
    
    
    draw = initDrawingSurface(screen)
    lst = generateButtons(screen, draw)
    lst.append(draw)
    #diag = initDialogueSurface(screen)
    run(screen, lst)
    quit()