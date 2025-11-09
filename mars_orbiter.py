"""
This module is the main executable of the Mars Orbiter game.

Author: Bryce Graffin
Date: 08 November 2025
"""
import os  # for updating where the window will be located if the user decides to exit fullscreen mode
import math  # for handling math calculations
import random  # for handling starting locations of the satellite sprite
import pygame as pg  # for running the game

# region === IMPORT MODULES FROM SRC ===
from src.utils.color_table import colors
from src.satellite import Satellite


def main():
    """
    Set up labels and instructions, create objects, & run the game loop.
    """
    pg.init()  # initializes pygame

    # set up the display
    os.environ['SDL_VIDEO_WINDOWS_POS'] = '700, 100'  # set origin of the game window and set to fullscreen
    screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)  # pylint: disable = no-member
    pg.display.set_caption('Mars Orbiter')
    background = pg.Surface(screen.get_size())

    pg.mixer.init()  # init the mixer for sound effects

    intro_text = [  # this will be displayed under the Satellite attribute labels at the top of window for 15 secs
        ' The Mars Orbiter experienced an error during Orbit insertion.',
        ' Use thrusters to correct to a circular mapping orbit without',
        ' running out of propellant or burning up in the atmosphere.'
    ]

    instruct_text1 = [  # this will be displayed in the top left of the display to instruct user on mission details
        'Orbital altitude must be within 69-120 miles',
        'Orbital Eccentricity must be < 0.05',
        'Avoid top of atmosphere at 68 miles'
    ]

    instruct_text2 = [  # this will be displayed in the bottom right of the display to instruct user on controls
        'Left Arrow = Decrease Dx',
        'Right Arrow = Increase Dx',
        'Up Arrow = Decrease Dy',
        'Down Arrow = Increase Dy',
        'Space Bar = Clear Path',
        'Escape = Exit Full Screen'
    ]

    # init the game objects
    sat = Satellite(background=background)
    sat_sprite = pg.sprite.Group(sat)

    # game loop
    clock = pg.time.Clock()  # for controlling frame rate

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:  # exit fullscreen mode
                    os.environ['SDL_VIDEO_WINDOW_POS'] = '700, 100'  # update window position
                    pg.display.set_mode((800, 600))  # set to windowed mode

        # update game objects
        sat_sprite.update()

        # draw
        screen.fill(colors['BLACK'])  # fill with black
        screen.blit(background, (0, 0))  # draw the background (which has the satellite path on it)
        sat_sprite.draw(screen)  # draw the satellite sprite
        sat_sprite

        pg.display.flip()
        clock.tick(60)  # cat at 60 FPS

    pg.quit()

if __name__ == '__main__':
    main()
