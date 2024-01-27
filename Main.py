import pygame as pg
from DrawingSurface import DrawSurface

# see if we can load more than standard BMP
if not pg.image.get_extended():
    raise SystemExit("Sorry, extended image module required")

# game constants
SCREENRECT = pg.Rect(0, 0, 640, 480)


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
    print(bestdepth)
    screen = pg.display.set_mode(SCREENRECT.size, winstyle | pg.SRCALPHA, bestdepth)
    
    # decorate the game window
    pg.display.set_caption("Pygame Demo")
    pg.mouse.set_visible(1)

    # create the background, tile the bgd image
    screen = pg.display.set_mode( SCREENRECT.size )
    screen.fill(pg.Color("white"))
    pg.display.flip()
    
    return screen
    

def initDrawingSurface(surf):
    pos = pg.Rect(SCREENRECT.size[0] * 0.3, SCREENRECT.size[1] * 0.1, SCREENRECT.size[0] * 0.65, SCREENRECT.size[1] * 0.65)
    res = DrawSurface(surf, pos)
    return res

def run(updatables):
    
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
        
        #update calls
        for u in updatables:
            u.update()
        
        #pygame_widgets.update(events)
        #pg.display.update(toolkitRect)
        pg.display.flip() #render call

        # cap the framerate at 40fps. Also called 40HZ or 40 times per second.
        clock.tick(60)
    

def quit():
    pg.time.wait(1000)
    pg.quit()


if __name__ == "__main__":
    screen = init()
    res = initDrawingSurface(screen)
    run([res])
    quit()