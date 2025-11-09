"""
This module contains the Satellite class and methods.

Author: Bryce Graffin
Date: 08 November 2025
"""
import os  # for updating where the window will be located if the user decides to exit fullscreen mode
import math  # for handling math calculations
import random  # for handling starting locations of the satellite sprite
import pygame as pg  # for running the game

# import utils
from src.utils.color_table import colors

class Satellite(pg.sprite.Sprite):
    """
    Satellite object that orbits the planet(s) and is controller by the player.
    """

    def __init__(self, background):
        super().__init__()
        
        self.background = background  # this is passed in and will be used to draw the satellite's path

        # load and convert both satellite state images (alive/crashed) and convert them to usable format upon init
        self.image_sat = pg.image.load(r"src\assets\sprites\satellite.png").convert()
        self.image_crash = pg.image.load(r"src\assets\sprites\satellite_crashed.png").convert()
        self.image = self.image_sat  # create ref
        self.image.set_colorkey(colors['BLACK'])

        # region === SETTING INITIAL POSITION, SPEED, FUEL, & SOUND ATTRIBUTES ===

        # set starting coords using random ranges
        self.x = random.randrange(315, 425)
        self.y = random.randrange(70, 180)

        # create the rectangle attribute of the Satellite sprite, use the black parts to remove the background
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)  # sets the starting position of the sprite

        # set starting velocity
        self.dx = random.choice([-3, 3])  # negative values result in counterclockwise orbit
        self.dy = 0  # this is handled by gravity

        # set heading (dish orientation), fuel, mass, and distance to the planet
        self.heading = 0
        self.fuel = 100
        self.mass = 1
        self.distance = 0

        # set starting sound attributes
        self.thrust = pg.mixer.Sound(r'src\assets\sounds\thrust_audio.ogg')
        self.thrust.set_volume(0.07)  # valid values are 0-1

        # endregion
