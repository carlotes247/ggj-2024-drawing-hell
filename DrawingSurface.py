import os
# import basic pygame modules
import pygame as pg

# see if we can load more than standard BMP
if not pg.image.get_extended():
    raise SystemExit("Sorry, extended image module required")

# game constants
SCREENRECT = pg.Rect(0, 0, 640, 480)

main_dir = os.path.split(os.path.abspath(__file__))[0]

#Tutorial Code
def load_image(file):
    """loads an image, prepares it for play"""
    file = os.path.join(main_dir, ".", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit(f'Could not load image "{file}" {pg.get_error()}')
    return surface.convert()


def compMinus(pos, offset):
    return (pos[0] - offset[0], pos[1] - offset[1])

def main(winstyle=0):
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
    screen = pg.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    # decorate the game window
    pg.display.set_caption("Pygame Demo")
    pg.mouse.set_visible(1)

    # create the background, tile the bgd image
    screen = pg.display.set_mode( SCREENRECT.size )
    screen.fill(pg.Color("white"))
    drawingSurfaceRect = pg.Rect(SCREENRECT.size[0] * 0.3, SCREENRECT.size[1] * 0.1, SCREENRECT.size[0] * 0.65, SCREENRECT.size[1] * 0.65)
    DrawingSurface = screen.subsurface(drawingSurfaceRect)
    DrawingSurface.fill(pg.Color("black"))
    
    pg.display.flip()

    clock = pg.time.Clock()
    # Run our main loop whilst the player is alive.
    while True:
        # get input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_f:
                    if not fullscreen:
                        print("Changing to FULLSCREEN")
                        screen_backup = screen.copy()
                        screen = pg.display.set_mode(
                            SCREENRECT.size, winstyle | pg.FULLSCREEN, bestdepth
                        )
                        screen.blit(screen_backup, (0, 0))
                    else:
                        print("Changing to windowed mode")
                        screen_backup = screen.copy()
                        screen = pg.display.set_mode(
                            SCREENRECT.size, winstyle, bestdepth
                        )
                        screen.blit(screen_backup, (0, 0))
                    pg.display.flip()
                    fullscreen = not fullscreen
        
        mouse_pressed = pg.mouse.get_pressed(num_buttons = 3)
        pos = pg.mouse.get_pos()
        if (drawingSurfaceRect.collidepoint(pos)):
            drawPos = compMinus(pos, drawingSurfaceRect)
            if (mouse_pressed[2]): #right button pressed
                pg.draw.circle(DrawingSurface, pg.Color("black"), drawPos, 20)
            elif (mouse_pressed[0]): #leftbutton pressed
                pg.draw.circle(DrawingSurface, pg.Color("white"), drawPos, 20)
        
        pg.display.flip() #render call

        # cap the framerate at 40fps. Also called 40HZ or 40 times per second.
        clock.tick(40)
    
    pg.time.wait(1000)


# call the "main" function if running this script
if __name__ == "__main__":
    main()
    pg.quit()
