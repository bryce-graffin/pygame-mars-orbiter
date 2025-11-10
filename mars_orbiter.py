"""
This module is the main executable of the Mars Orbiter game.

Author: Bryce Graffin
Date: 08 November 2025
"""
# region === IMPORTS ===
# generic imports
import os  # for updating where the window will be located if the user decides to exit fullscreen mode
import pygame as pg  # for running the game

# module imports
from src.utils.color_table import colors
from src.utils.game_window import instructions_label, box_label
from src.utils.calculations import calculate_eccentricity
from src.satellite import Satellite
from src.planet import Planet

# endregion

# TODO: add a Scene object to contain this main game loop and related methods
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

    instructions_text1 = [  # this will be displayed in the top left of the display to instruct user on mission details
        'Orbital altitude must be within 69-120 miles',
        'Orbital Eccentricity must be < 0.05',
        'Avoid top of atmosphere at 68 miles'
    ]

    instructions_text2 = [  # this will be displayed in the bottom right of the display to instruct user on controls
        'Left Arrow = Decrease Dx',
        'Right Arrow = Increase Dx',
        'Up Arrow = Decrease Dy',
        'Down Arrow = Increase Dy',
        'Space Bar = Clear Path',
        'Escape = Exit Full Screen'
    ]

    # init the game objects
    planet_obj = Planet()
    planet_sprite = pg.sprite.Group(planet_obj)
    sat_obj = Satellite(background=background)
    sat_sprite = pg.sprite.Group(sat_obj)

    # init orbit verification variables
    dist_list = []  # list of distances from planet center to satellite at each frame
    eccentricity = 1.0  # initial eccentricity value
    eccentricity_calc_interval = 5  # calculate eccentricity every 5 frames

    # satellite mapping functionality upon win
    mapping_enabled = False

    # time keeping
    clock = pg.time.Clock()  # for controlling frame rate
    fps = 60
    tick_count = 0  # count the number of ticks for timing events

    # main game loop
    running = True
    while running:
        clock.tick(fps)
        tick_count += 1
        dist_list.append(sat_obj.distance)

        # region === GET KEYBOARD INPUTS ===

        for event in pg.event.get():
            if event.type == pg.QUIT:  # close window
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:  # exit fullscreen mode
                    os.environ['SDL_VIDEO_WINDOW_POS'] = '700, 100'  # update window position
                    pg.display.set_mode((800, 600))  # set to windowed mode

                elif event.key == pg.K_SPACE:  # clear the satellite path
                    background.fill(colors['BLACK'])

                elif event.type == pg.KEYUP:  # stop thrust sound when key is released
                    sat_obj.thrust.stop()  # turn off the mapping view

                elif mapping_enabled:  # turn on mapping view if win conditions met
                    if event.type == pg.KEYDOWN and event.key == pg.K_m:
                        planet_obj.mapping_on(planet_obj)

        # endregion

        # region === APPLYING PHYSICS & CHECKING WIN CONDITIONS ===

        # get heading & distance to planet & apply gravity
        sat_obj.locate(planet=planet_obj)
        planet_obj.gravity(satellite=sat_obj)

        # calculate eccentricity at set intervals
        if tick_count % (eccentricity_calc_interval * fps) == 0:
            eccentricity = calculate_eccentricity(dist_list=dist_list)
            dist_list = []  # reset distance list after calculation

        # re-blit background for drawing command - prevents clearing path
        screen.blit(background, (0, 0))

        # fuel/altitude fail conditions
        if sat_obj.fuel <= 0:
            instructions_label(
                screen=screen,
                text=['FUEL DEPLETED! MISSION FAILED.'],
                color=colors['RED'],
                x=340,
                y=195
            )
            sat_obj.fuel = 0  # prevent negative fuel display
            sat_obj.dx = 2  # force escape trajectory; potential future improvement: dont' fly off but instead crash
        elif sat_obj.distance <= 68:
            instructions_label(
                screen=screen,
                text=['ORBIT DECAY - ENTERING ATMOSPHERE! MISSION FAILED.'],
                color=colors['RED'],
                x=340,
                y=195
            )
            sat_obj.image = sat_obj.image_crash  # change to crashed image
            sat_obj.dx = 0
            sat_obj.dy = 0


        # endregion

        # update game objects
        sat_sprite.update()
        planet_sprite.update()

        # draw
        screen.fill(colors['BLACK'])  # fill with black
        screen.blit(background, (0, 0))  # draw the background (which has the satellite path on it)
        sat_sprite.draw(screen)  # draw the satellite sprite

        pg.display.flip()
        clock.tick(60)  # cat at 60 FPS

    pg.quit()

if __name__ == '__main__':
    main()
